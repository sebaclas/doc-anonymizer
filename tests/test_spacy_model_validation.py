"""
Tests for spaCy model validation in config and ner modules.

Covers:
- 3.1 Settings.load() filters models not installed in the environment
- 3.2 Settings.load() falls back gracefully when get_installed_models() raises
- 3.3 ner._load_model() RuntimeError message lists the attempted models
"""
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_settings(tmp_path: Path, ner_models: list[str]) -> Path:
    """Write a minimal settings.json to tmp_path and return its path."""
    settings_file = tmp_path / "settings.json"
    settings_file.write_text(
        json.dumps({"ner_models": ner_models}),
        encoding="utf-8",
    )
    return settings_file


# ---------------------------------------------------------------------------
# 3.1  Settings.load() filters models not installed in the environment
# ---------------------------------------------------------------------------

class TestFilterInstalledNerModels:
    def test_invalid_models_are_removed(self, tmp_path):
        """Models absent from the environment must be stripped from the list."""
        settings_file = _write_settings(
            tmp_path, ["xx_ent_wiki_sm", "es_core_news_lg"]
        )

        with patch("spacy.util.get_installed_models", return_value=["es_core_news_lg"]):
            from anonymizer.config import Settings
            s = Settings.load(settings_file)

        assert s.ner_models == ["es_core_news_lg"]

    def test_all_valid_models_are_kept(self, tmp_path):
        """When all configured models are installed, none should be removed."""
        settings_file = _write_settings(
            tmp_path, ["es_core_news_lg", "es_core_news_sm"]
        )

        with patch(
            "spacy.util.get_installed_models",
            return_value=["es_core_news_lg", "es_core_news_sm"],
        ):
            from anonymizer.config import Settings
            s = Settings.load(settings_file)

        assert s.ner_models == ["es_core_news_lg", "es_core_news_sm"]

    def test_empty_list_when_none_installed(self, tmp_path):
        """If no configured model is installed, ner_models must end up empty."""
        settings_file = _write_settings(
            tmp_path, ["xx_ent_wiki_sm", "es_core_news_sm"]
        )

        with patch("spacy.util.get_installed_models", return_value=[]):
            from anonymizer.config import Settings
            s = Settings.load(settings_file)

        assert s.ner_models == []


# ---------------------------------------------------------------------------
# 3.2  Settings.load() falls back gracefully when get_installed_models() raises
# ---------------------------------------------------------------------------

class TestFilterFallbackOnError:
    def test_original_list_preserved_when_api_raises(self, tmp_path):
        """If get_installed_models() fails, the original list must be kept intact."""
        models = ["xx_ent_wiki_sm", "es_core_news_lg"]
        settings_file = _write_settings(tmp_path, models)

        with patch(
            "spacy.util.get_installed_models",
            side_effect=RuntimeError("API unavailable"),
        ):
            from anonymizer.config import Settings
            s = Settings.load(settings_file)

        assert s.ner_models == models


# ---------------------------------------------------------------------------
# 3.3  ner._load_model() RuntimeError message lists the attempted models
# ---------------------------------------------------------------------------

class TestNerLoadModelErrorMessage:
    def test_error_lists_attempted_models(self):
        """RuntimeError must include the model names that were tried."""
        # Ensure spacy.load always fails (simulates no models installed in exe)
        with patch("spacy.load", side_effect=OSError("model not found")):
            # Patch current_settings so we control which models are attempted
            mock_settings = MagicMock()
            mock_settings.ner_models = ["model_a", "model_b"]
            mock_settings.ner_stopwords = []

            with patch("anonymizer.detectors.ner.current_settings", mock_settings):
                import anonymizer.detectors.ner as ner_module
                # Reset cached model to force re-load
                ner_module._nlp = None

                with pytest.raises(RuntimeError) as exc_info:
                    ner_module._load_model()

        error_msg = str(exc_info.value)
        assert "model_a" in error_msg
        assert "model_b" in error_msg

    def test_error_message_when_no_models_configured(self):
        """RuntimeError must handle an empty models list gracefully."""
        with patch("spacy.load", side_effect=OSError("model not found")):
            mock_settings = MagicMock()
            mock_settings.ner_models = []
            mock_settings.ner_stopwords = []

            with patch("anonymizer.detectors.ner.current_settings", mock_settings):
                import anonymizer.detectors.ner as ner_module
                ner_module._nlp = None

                with pytest.raises(RuntimeError) as exc_info:
                    ner_module._load_model()

        error_msg = str(exc_info.value)
        assert "(ninguno)" in error_msg
