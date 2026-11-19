from whisper import MODEL_ALIASES, translate_args

TURBO = MODEL_ALIASES["turbo"]


def test_openai_style_command():
    assert translate_args(["video.mp4", "--model", "turbo", "--output_format", "txt"]) == [
        "video.mp4", "--model", TURBO, "--output-format", "txt",
    ]


def test_defaults_to_turbo_and_auto_detects_language():
    assert translate_args(["a.mp3"]) == ["a.mp3", "--model", TURBO]


def test_model_alias_with_equals():
    assert translate_args(["a.mp3", "--model=small.en"]) == [
        "a.mp3", "--model=mlx-community/whisper-small.en-mlx",
    ]


def test_full_repo_name_and_values_are_untouched():
    args = ["a.mp3", "--model", "mlx-community/foo_bar", "--output_dir", "my_out"]
    assert translate_args(args) == [
        "a.mp3", "--model", "mlx-community/foo_bar", "--output-dir", "my_out",
    ]


def test_default_language_applies_only_without_flag():
    assert translate_args(["a.mp3"], "en")[-2:] == ["--language", "en"]
    assert translate_args(["a.mp3", "--language", "fr"], "en") == [
        "a.mp3", "--language", "fr", "--model", TURBO,
    ]


def test_hardware_flags_are_dropped_with_their_values():
    args = ["a.mp3", "--device", "cuda", "--fp16", "False", "--threads=4", "--task", "translate"]
    assert translate_args(args) == ["a.mp3", "--task", "translate", "--model", TURBO]


def test_ignored_flag_without_value_does_not_swallow_next_flag():
    assert translate_args(["a.mp3", "--fp16", "--task", "translate"]) == [
        "a.mp3", "--task", "translate", "--model", TURBO,
    ]
