from lingua import Language, LanguageDetectorBuilder

def check_language(text):
    detector = LanguageDetectorBuilder.from_all_languages().with_preloaded_language_models().build()
    confidence_value = detector.compute_language_confidence(text, Language.ENGLISH)
    return confidence_value
