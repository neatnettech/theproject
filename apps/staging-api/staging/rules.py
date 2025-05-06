class PromotionRules:
    """
    rules that can be applied in beteen stages (stage -> revision -> production)
    """
    #TODO: some of these makes not much sense as of now
    def validate_promotion(self, command, record, target_stage):
        pass