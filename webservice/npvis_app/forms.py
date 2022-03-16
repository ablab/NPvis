import json

from django import forms

class NPvisForm(forms.Form):
    CHOICES_MODE = [("PNP", "PNP"), ("PNPmd", "PNP with modification")]
    CHOICES_MS_INPUT = [("mgf", "File(MGF/mzXML/mzML)"), ("gusi", "GNPS USI")]
    CHOICES_STRUCT_INPUT = [("mol", "File(MOL)"), ("smiles", "SMILES")]
    CHOICES_ERROR_TYPE = [("absolute", "Da"), ("relative", "ppm")]
    CHOICES_ADDUCT_TYPE = [("H", "H"), ("Na", "Na"), ("K", "K")]

    mode_type = forms.ChoiceField(widget=forms.Select, choices=CHOICES_MODE)
    ms_input_type = forms.ChoiceField(widget=forms.Select, choices=CHOICES_MS_INPUT)
    struct_input_type = forms.ChoiceField(widget=forms.Select, choices=CHOICES_STRUCT_INPUT)
    error_type = forms.ChoiceField(widget=forms.Select, choices=CHOICES_ERROR_TYPE)
    adduct_type = forms.ChoiceField(widget=forms.Select, choices=CHOICES_ADDUCT_TYPE)

    file_spectrum = forms.FileField(required=False)
    file_structure = forms.FileField(required=False)

    error_threshold = forms.FloatField(required=False)
    scanId = forms.IntegerField(required=False)
    charge_val = forms.IntegerField(required=False)
    compound_name = forms.CharField(required=False)
    smiles = forms.CharField(required=False)
    gusi = forms.CharField(required=False)



    def save_json(self, out_filename):
        self.is_valid()
        field_dict = self.cleaned_data.copy()
        try:
            field_dict["file_spectrum"] = self.cleaned_data["file_spectrum"].name
        except:
            field_dict["file_spectrum"] = ""

        try:
            field_dict["file_structure"] = self.cleaned_data["file_structure"].name
        except:
            field_dict["file_structure"] = ""

        with open(out_filename, "w") as f:
            json.dump(field_dict, f)