class HeightWeightNormalizer:
    def __init__(self, elements):
        self.elements = elements

    def normalize_height_weight(self):
        """
        Function to return a normalise height and weight to be standardised
        :param element: element from the csv that ca be height or weight
        :return: height and weight in cm and kg without the unit
        """
        new_element = None

        element = self.elements[0]

        if "cm" in element or "kg" in element:
            try:
                new_element = float(
                    element.replace("cm", "").replace("kg", "").strip()
                )
            except ValueError:
                pass
        elif float(element) < 3:
            try:
                new_element = float(element) * 100
            except ValueError:
                pass
        else:
            try:
                new_element = float(element)
            except ValueError:
                pass

        return [str(new_element)]
