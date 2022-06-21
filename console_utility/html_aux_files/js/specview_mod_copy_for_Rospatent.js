$(function() {
    // plugin name - specview_dereplicator
    	$.fn.specview_dereplicator = function (opts) {

        var defaults = {
                ...
        };

        var options = $.extend(true, {}, defaults, opts); // this is a deep copy
        var nonSelectedSpecs, selectedSpecs, modifiedSpecs, modSelectedSpecs, invisibleSpecs, fragmentedBondsSpecs;

        return this.each(function() {
            index = index + 1;
            init($(this), options);
        });
    };

    var index = 0;
    var massErrorType_Da = 'Da';
    var massErrorType_ppm = 'ppm';

    var elementIds = {
            ...
    };

    var molColors = {
        'default': 'black',
        'selected': 'blue',
        'modified': '#ff9933',
        'mod_selected': '#00ccff'
    };

    ...

    function defineBonds() {
        nonSelectedSpecs = new ChemDoodle.structures.VisualSpecifications();
        nonSelectedSpecs.bonds_color = molColors['default'];
        nonSelectedSpecs.atoms_color = molColors['default'];
        selectedSpecs = new ChemDoodle.structures.VisualSpecifications();
        selectedSpecs.bonds_color = molColors['selected'];
        selectedSpecs.atoms_color = molColors['selected'];
        modifiedSpecs = new ChemDoodle.structures.VisualSpecifications();
        modifiedSpecs.bonds_color = molColors['modified'];
        modifiedSpecs.atoms_color = molColors['modified'];
        modSelectedSpecs = new ChemDoodle.structures.VisualSpecifications();
        modSelectedSpecs.bonds_color = molColors['mod_selected'];
        modSelectedSpecs.atoms_color = molColors['mod_selected'];
        invisibleSpecs = new ChemDoodle.structures.VisualSpecifications();
        invisibleSpecs.bonds_color = 'white';
        invisibleSpecs.atoms_color = 'white';
        fragmentedBondsSpecs = new ChemDoodle.structures.VisualSpecifications();
        fragmentedBondsSpecs.bonds_color = 'red';
    }

    function init(parent_container, options) {
        options.annotation = sortByKey(options.annotation, 'peakIdx');  // i.e. sorting by 'mz'
        var peaksGroups = splitPeaks(options.spectrum, options.annotation);
        options.notMatchedPeaks = peaksGroups[0];
        options.matchedPeaks = peaksGroups[1];

        options.massErrorsDa = calcMassErrors(options.matchedPeaks, options.annotation,
            massErrorType_Da);
        options.massErrorsPpm = calcMassErrors(options.matchedPeaks, options.annotation,
            massErrorType_ppm);
        refreshMassErrors(options);

        if (options.spectrumInfo || options.compoundInfo)
            addGeneralInfoPanel(parent_container, options);

        var container = createContainer(parent_container);
        // alert(container.attr('id')+" parent "+container.parent().attr('id'));
        storeContainerData(container, options);
        initContainer(container);
        defineBonds();

        makeViewingOptions(container, options);

        if(options.sequence) {
            showSequenceInfo(container, options);
        }

        createPlot(container, getDatasets(container)); // Initial MS/MS Plot

        setupInteractions(container, options);
        if (options.mol) showNewMol(options.mol, options);
        addMatchedPeaksTable(container);
    }

    function splitPeaks(spectrum, annotation) {
        var allPeakIdx = 0;
        var matchedPeakIdx = 0;
        var curMatchedPeakInfo = matchedPeakIdx < annotation.length ?
            annotation[matchedPeakIdx] : null;
        var notMatchedPeaks = [];
        var matchedPeaks = [];
        while (allPeakIdx < spectrum.length) {
            if (curMatchedPeakInfo && curMatchedPeakInfo.peakIdx == allPeakIdx) {
                matchedPeaks.push(spectrum[allPeakIdx]);
                matchedPeakIdx++;
                curMatchedPeakInfo = matchedPeakIdx < annotation.length ? annotation[matchedPeakIdx] : null;
            } else {
                notMatchedPeaks.push(spectrum[allPeakIdx]);
            }
            allPeakIdx++;
        }
        return [notMatchedPeaks, matchedPeaks];
    }

    ...

    function storeContainerData(container, options) {
        container.data("index", index);
        container.data("options", options);
        container.data("massErrorChanged", false);
        container.data("massTypeChanged", false);
        container.data("plot", null);           // MS/MS plot
        container.data("zoomRange", null);      // for zooming MS/MS plot
        container.data("previousPoint", null);  // for tooltips
        container.data("massError", 0.0);

        var maxInt = getMaxInt(options);
        var __xrange = getPlotXRange(options);
        var plotOptions =  {
                series: {},
                selection: { mode: "x", color: "#F0E68C" },
                grid: { show: true,
                        hoverable: true,
                        autoHighlight: false,
                        clickable: true,
                        borderWidth: 1,
                        labelMargin: options.labelMargin },
                xaxis: { tickLength: 3, tickColor: "#000",
                         min: __xrange.xmin,
                         max: __xrange.xmax},
                yaxis: { tickLength: 0, tickColor: "#000",
                         max: maxInt*1.1,
                         labelWidth: options.labelWidth,
                         ticks: [0, maxInt*0.1, maxInt*0.2, maxInt*0.3, maxInt*0.4, maxInt*0.5,
                                 maxInt*0.6, maxInt*0.7, maxInt*0.8, maxInt*0.9, maxInt],
                         tickFormatter: function(val, axis) {return Math.round((val * 100)/maxInt)+"%";}}
            };
        container.data("plotOptions", plotOptions);
        container.data("maxInt", maxInt);

    }

    ...

    // -----------------------------------------------
    // SET UP INTERACTIVE ACTIONS FOR MS/MS PLOT
    // -----------------------------------------------
    function setupInteractions (container, options) {

        // ZOOMING
        $(getElementSelector(container, elementIds.msmsplot)).bind("plotselected", function (event, ranges) {
            container.data("zoomRange", ranges);
            reloadPlotWithSelection(container, options);
        });

        // ZOOM AXES
        $(getElementSelector(container, elementIds.zoom_x)).click(function() {
            resetAxisZoom(container);
        });
        $(getElementSelector(container, elementIds.zoom_y)).click(function() {
            resetAxisZoom(container);
        });

        // RESET ZOOM
        $(getElementSelector(container, elementIds.resetZoom)).click(function() {
            resetZoom(container, options);
        });

        // UPDATE
        $(getElementSelector(container, elementIds.update)).click(function() {
            container.data("zoomRange", null); // zoom out fully
            setMassError(container);
            createPlot(container, getDatasets(container));
        });

        $(getElementSelector(container, elementIds.msmsplot)).bind("plotclick", function (event, pos, item) {
                var plotOptions = container.data("options");
                if (item) {
                    var selectedPeakIdx = -1;
                    for (var i = 0; i < plotOptions.matchedPeaks.length; i++) {
                        if(item.datapoint[0] == plotOptions.matchedPeaks[i][0]) {
                            selectedPeakIdx = i;
                            break;
                        }
                    }
                    if (selectedPeakIdx != -1){
                        selectGroup(container, selectedPeakIdx, plotOptions);
                        container.data("options", plotOptions);
                        createPlot(container, getDatasets(container, plotOptions.matchedPeaks[selectedPeakIdx]));
                    }
                }
            });
        $(getElementSelector(container, elementIds.enableTooltip)).click(function() {
            $(getElementSelector(container, elementIds.msmstooltip)).remove();
        });

        // PLOT MASS ERROR CHECKBOX
        $(getElementSelector(container, elementIds.massErrorPlot_option)).click(function() {
            var plotDiv = $(getElementSelector(container, elementIds.massErrorPlot));
            if($(this).is(':checked'))
            {
                plotDiv.show();
                plotPeakMassErrorPlot(container, getDatasets(container));
                container.data("options").showMassErrorPlot = true;
            }
            else
            {
                plotDiv.hide();
                container.data("options").showMassErrorPlot = false;
            }
        });

        // CHANGING THE PLOT SIZE
        makePlotResizable(container);

	    // PRINT SPECTRUM
	    savePlot(container);
    }

    ...

    function showNewMol(mol, options) {
        var fragmentedBonds = options.fragmentedBonds;
        for(var i = 0; i < mol.atoms.length; i++) {
            var atomComponentId = options.atomComponents[i];
            if (isComponentModified(options, atomComponentId)) {
                mol.atoms[i].specs = modifiedSpecs;
            }
            else mol.atoms[i].specs = nonSelectedSpecs;
        }
        for(var i = 0; i < mol.bonds.length; i++) {
            var b = mol.bonds[i];
            if (fragmentedBonds.indexOf(i) != -1) {
                b.specs = fragmentedBondsSpecs;
            }
            else if (b.a1.specs == modifiedSpecs && b.a2.specs == modifiedSpecs) {
                b.specs = modifiedSpecs;
            }
            else b.specs = nonSelectedSpecs;
        }
        options.canvas.loadMolecule(mol);
        return mol;
    }

    function resetSelection(container) {
        var options = container.data("options");

        if (options.selectedPeak != null) {
            var matchedPeadId = getElementId(container, elementIds.peakRow) + '_' + options.selectedPeak;
            $('#' + matchedPeadId).removeClass('selected_row');
            options.selectedPeak = null;

            if (options.mol) {
                showNewMol(options.mol, options);
            }
            else {
                $(getElementSelector(container, elementIds.seqCanvas)).html(getModifiedSequence(options));
            }
            createPlot(container, getDatasets(container));
            $(getElementSelector(container, elementIds.currentMass))
                .text('Select a colored peak to view annotation');
        }
    }

    function selectGroup(container, matchedPeakIdx, options) {
        options.selectedPeak = matchedPeakIdx;
        var mz = options.matchedPeaks[matchedPeakIdx][0];
        var intensity = options.matchedPeaks[matchedPeakIdx][1];
        var massError = options.massErrors[matchedPeakIdx];
        var charge = options.annotation[matchedPeakIdx].charge;
        var components = options.annotation[matchedPeakIdx].components;

        // clearing selection for other peaks
        for (var i = 0; i < options.matchedPeaks.length; i++) {
            $('#' + getElementId(container, elementIds.peakRow) + '_' + i).attr('class', '');
        }

        var matchInfo = [];
        matchInfo.push(parseFloat(mz).toFixed(options.precision));
        matchInfo.push(parseFloat(massError).toFixed(getMassErrorPrecision(options)));
        matchInfo.push(charge);
        matchInfo.push(parseFloat(intensity).toFixed(options.precision));
        var matchedPeadId = getElementId(container, elementIds.peakRow) + '_' + matchedPeakIdx;
        $('#' + matchedPeadId).addClass('selected_row');
        //document.getElementById(matchedPeadId).scrollIntoView(true);

        if (options.mol)
            selectGroupInMol(components, options);
        else
            selectGroupInSeq(container, components, options);
        $(getElementSelector(container, elementIds.currentMass)).text(
            matchInfoToString(matchInfo, options.massErrorUnit));
    }

    function matchInfoToString(matchInfo, unit) {
        return "M/z: " + matchInfo[0] + " Da/e, " + "mass error: " + matchInfo[1] +
            " " + unit + ", charge: " + matchInfo[2] + ", intensity: " + matchInfo[3];
    }

    function selectGroupInSeq(container, components, options) {
        $(getElementSelector(container, elementIds.seqCanvas)).html(getModifiedSequence(options, components));
    }

    function selectGroupInMol(components, options) {
        var mol = options.mol;
        var fragmentedBonds = options.fragmentedBonds;
        for (var i = 0; i < mol.atoms.length; i++) {
            var atomComponentId = options.atomComponents[i];
            var isSelected = components.indexOf(atomComponentId) != -1;
            var isModified = isComponentModified(options, atomComponentId);
            if (isModified && isSelected) {
                mol.atoms[i].specs = modSelectedSpecs;
            }
            else if (isModified) {
                mol.atoms[i].specs = modifiedSpecs;
            }
            else if (isSelected) {
                mol.atoms[i].specs = selectedSpecs;
            }
            else mol.atoms[i].specs = nonSelectedSpecs;
        }
        for (var i = 0; i < mol.bonds.length; i++) {
            var b = mol.bonds[i];
            if (b.a1.specs == invisibleSpecs || b.a2.specs == invisibleSpecs)
                b.specs = invisibleSpecs;
            else if (fragmentedBonds.indexOf(i) != -1)
                b.specs = fragmentedBondsSpecs;
            else if (b.a1.specs == modifiedSpecs && b.a2.specs == modifiedSpecs)
                b.specs = modifiedSpecs;
            else if (b.a1.specs == modSelectedSpecs && b.a2.specs == modSelectedSpecs)
                b.specs = modSelectedSpecs;
            else if (b.a1.specs == selectedSpecs && b.a2.specs == selectedSpecs)
                b.specs = selectedSpecs;
            else b.specs = nonSelectedSpecs;
        }
        options.canvas.loadMolecule(mol);
    }

    function addMatchedPeaksTable(container) {
        var options = container.data("options");

        var matchInfos = [];
        for (var matchedPeakIdx = 0; matchedPeakIdx < options.annotation.length; matchedPeakIdx++) {
            var mz = options.matchedPeaks[matchedPeakIdx][0];
            var intensity = options.matchedPeaks[matchedPeakIdx][1];
            var massError = options.massErrors[matchedPeakIdx];
            var charge = options.annotation[matchedPeakIdx].charge;

            var matchInfo = [];
            matchInfo.push(parseFloat(mz).toFixed(options.precision));
            matchInfo.push(parseFloat(massError).toFixed(getMassErrorPrecision(options)));
            matchInfo.push(charge);
            matchInfo.push(parseFloat(intensity).toFixed(options.precision));
            matchInfos.push(matchInfo);
        }

        var peaksTable = '' ;
        peaksTable += '<div id="' + getElementId(container, elementIds.peaksTable) + '" align="center">';
        peaksTable += '<h4 class="annoPeaksHeader">Annotated peaks</h4>';
        peaksTable += '<table id="table_scroll" cellpadding="1" class="font_small ' + 'annoPeaksTable' + '">';
        peaksTable +=  '<thead>';
        peaksTable +=   "<tr>";
        var headersPeaksTable = ["M/z (Da/e)", "Mass error (" + options.massErrorUnit + ")",
            "Charge", "Intensity"];

        for(var i = 0; i < headersPeaksTable.length; i += 1) {
            peaksTable += '<th>' + headersPeaksTable[i] +  '</th>';
        }
        peaksTable += "</tr>";
        peaksTable += "</thead>";

        if (options.mol)
            peaksTable += '<tbody style="height: 170px;">';
        else
            peaksTable += '<tbody style="height: 370px;">';

        for(var i = 0; i < matchInfos.length; i += 1) {
            peaksTable +=   '<tr id="' + getElementId(container, elementIds.peakRow) + '_' + i + '">';
            for (var j = 0; j < matchInfos[i].length; j++){
                peaksTable += "<td>" + matchInfos[i][j] +  "</td>";
            }
            peaksTable += "</tr>";
        }

        peaksTable += "</tbody>";
        peaksTable += "</table>";
        peaksTable += "</div>";

        $(getElementSelector(container, elementIds.peaksTable)).remove();
        $(getElementSelector(container, elementIds.peaksTableDiv)).prepend(peaksTable);

        if ( options.sizeChangeCallbackFunction ) {
            options.sizeChangeCallbackFunction();
        }
    }

    ...

    function reloadPlotWithSelection(container, options) {
        if (options.selectedPeak) {
            plotOptions = container.data("options");
            createPlot(container, getDatasets(container, plotOptions.matchedPeaks[options.selectedPeak]));
        }
        else {
            createPlot(container, getDatasets(container));
        }
    }

    function plotAccordingToChoices(container) {
        var data = getDatasets(container);

        if (data.length > 0) {
            createPlot(container, data);
            showSequenceInfo(container); // update the MH+ and m/z values
        }
    }

    ...

    function getDatasets(container, selectedPeak) {

        var options = container.data("options");

        var data = [{data: options.notMatchedPeaks, color: '#C0C0C0', bars: {
                        show: true,
                        fill: 1,
                        barWidth: 2,
                        lineWidth: 0.5,
                        fillColor:  "#C0C0C0",
                        align: 'center'
                    }, clickable: false, hoverable: false},
                    {data: options.matchedPeaks, color: '#00CCFF', bars: {
                        show: true,
                        fill: 1,
                        lineWidth: 0.5,
                        color: '#66CCFF',
                        barWidth: 3,
                        align: 'center'
                    }}];
        if (selectedPeak){
            var d = {data: [selectedPeak], color: '#0000FF', bars: {
                        show: true,
                        fill: 1,
                        lineWidth: 0.5,
                        color: '#0000FF',
                        barWidth: 3,
                        align: 'center'}};
            data.push(d);
        }

        return data;
    }

    function processInfoField(field, unit, precision) {
        if (unit)
            unit = ' ' + unit;
        else
            unit = '';
        return (field || field === 0) ? (precision ? field.toFixed(precision) : field) + unit : 'N/A';
    }

    ...

    function initContainer(container) {

        var options = container.data("options");

        var rowspan = 2;

        var parentTable = '<table cellpadding="0" cellspacing="5" class="lorikeet-outer-table"> ';
        parentTable += '<tbody> ';

        if(options.sequence) {
            // placeholder for sequence, m/z, scan number etc
            parentTable += '<td colspan="2" style="background-color: white; padding:5px; border:1px dotted #cccccc;" valign="bottom" align="center"> ';
            parentTable += '<div id="'+getElementId(container, elementIds.seqinfo)+'" style="width:100%;"></div> ';
            parentTable += '</td> ';
        }

        // placeholders for the ms/ms plot
        parentTable += '<tr> ';
        parentTable += '<td style="background-color: white; padding:5px; border:1px dotted #cccccc;width:'+options.width+'px;height:'+options.height+'px;" valign="top" align="center"> ';
        // placeholder for peak mass error plot
        parentTable += '<div id="'+getElementId(container, elementIds.msmsplot)+'" align="bottom" style="width:'+options.width+'px;height:'+options.height+'px;"></div> ';
        parentTable += '<div id="'+getElementId(container, elementIds.viewOptionsDiv)+'" style="margin-top:15px;"></div> ';
        parentTable += '<div id="'+getElementId(container, elementIds.currentMass)+'" style="margin-top:15px;">Select a colored peak to view annotation</div> ';
        // placeholder for viewing options (zoom, plot size etc.)
        parentTable += '<div id="'+getElementId(container, elementIds.massErrorPlot)+'" style="width:'+options.width+'px;height:90px;"></div> ';
        parentTable += '</td> ';
        parentTable += '<td style="background-color: white; padding:5px; border:1px dotted #cccccc;width:" valign="top" align="center"> ';
        if (options.modification) {
            parentTable += modificationInfoToString(options.modification, options.precision);
        }
        parentTable += '<canvas id="' + getElementId(container, elementIds.chemCanvas) + '" align="top"></canvas>';
        if (options.mol) {
            parentTable += '<div style="margin-bottom: 20px;"><span class="span_tip">Click and use mouse to roll and zoom the structure</span></div>';
        }

        parentTable += '<div id="'+ getElementId(container, elementIds.peaksTableDiv) +'" align="top"></div> ';
        parentTable += '</td> ';
        parentTable += '</tr> ';

        parentTable += '</tbody> ';
        parentTable += '</table> ';

        container.append(parentTable);
        if (options.mol) {
            var myCanvas = new ChemDoodle.TransformCanvas('' + getElementId(container, elementIds.chemCanvas), 550, 250);
            myCanvas.emptyMessage = 'No Data Loaded!';
            myCanvas.loadMolecule(options.mol);
            options.canvas = myCanvas;
        }
        else {
            $('#' + getElementId(container, elementIds.chemCanvas)).hide();
        }
        return container;
    }

    //---------------------------------------------------------
    // SEQUENCE INFO
    //---------------------------------------------------------
    function showSequenceInfo (container) {
        var options = container.data("options");

        var specinfo = '';
        if(options.sequence) {
            specinfo += '<div>';
            specinfo += '<p style="font-weight:bold; color:#8B0000;" id="' + getElementId(container, elementIds.seqCanvas) + '">' + getModifiedSequence(options) + '</p>';
            specinfo += '</div>';
        }

        // first clear the div if it has anything
        $(getElementSelector(container, elementIds.seqinfo)).empty();
        $(getElementSelector(container, elementIds.seqinfo)).append(specinfo);
    }

    function getModifiedSequence(options, proteinArray) {
        var modSeq = '';
        var lettersCounter = 0;
        var altLetters = [];
        var altPattern = /\w[-+]\d/ig;
        while (result = altPattern.exec(options.sequence)) {
            altLetters.push(result.index);
        }
        for(var i = 0; i < options.sequence.length; i += 1) {
            currentChar = options.sequence.charAt(i);
            if (currentChar.match(/[A-Z]/i)) lettersCounter += 1;
            isAltLetter = altLetters.indexOf(i) != -1 || !currentChar.match(/[A-Z]/i);
            isSelected = proteinArray && proteinArray.indexOf(lettersCounter - 1) != -1;
            if (isAltLetter && isSelected)
                modSeq += highlightSequence(currentChar, '#00ccff');
            else if (isSelected)
                modSeq += highlightSequence(currentChar, 'blue');
            else if (isAltLetter)
                modSeq += highlightSequence(currentChar, 'red');
            else modSeq += currentChar;
        }
        return modSeq;
    }

    function highlightSequence(seq, color) {
        return '<span style="color: ' + color + ';">' + seq + '</span>';
    }

    function modificationInfoToString(modification, precision) {
        var massShiftSign = modification.massShift > 0 ? ' + ' : ' - ';
        var massShiftStr = massShiftSign + Math.abs(modification.massShift).toFixed(precision);
        var componentActualMass = Math.max(0, modification.componentMass + modification.massShift).toFixed(precision);
        var lossAA = componentActualMass < Ion.MASS_PROTON ? ' (loss of AA)' : '';
        return '<div id="mass_shift_div" align="left" style="padding-left: 20px; padding-top: 10px;z-index: 1000;">' +
                '<span style="font-weight:bold;">' +
                'Modification: <span style="color: ' + molColors['modified'] + ';">' +
                modification.componentFormula + massShiftStr + ' Da = ' +
                componentActualMass + ' Da</span>' + lossAA + '</div>';
    }

    ...

});
