"""`whisper` command that accepts openai-whisper style arguments and runs mlx-whisper."""

import sys

DEFAULT_MODEL = "turbo"
DEFAULT_LANGUAGE = "en"

MODEL_ALIASES = {
    "tiny": "mlx-community/whisper-tiny-mlx",
    "tiny.en": "mlx-community/whisper-tiny.en-mlx",
    "base": "mlx-community/whisper-base-mlx",
    "base.en": "mlx-community/whisper-base.en-mlx",
    "small": "mlx-community/whisper-small-mlx",
    "small.en": "mlx-community/whisper-small.en-mlx",
    "medium": "mlx-community/whisper-medium-mlx",
    "medium.en": "mlx-community/whisper-medium.en-mlx",
    "large-v2": "mlx-community/whisper-large-v2-mlx",
    "large-v3": "mlx-community/whisper-large-v3-mlx",
    "large": "mlx-community/whisper-large-v3-mlx",
    "large-v3-turbo": "mlx-community/whisper-large-v3-turbo",
    "turbo": "mlx-community/whisper-large-v3-turbo",
}


def translate_args(args: list[str]) -> list[str]:
    """Rewrite openai-whisper style arguments into mlx_whisper ones."""
    out: list[str] = []
    flags: set[str] = set()
    model_value_next = False

    for arg in args:
        if model_value_next:
            out.append(MODEL_ALIASES.get(arg, arg))
            model_value_next = False
            continue

        if not arg.startswith("--"):
            out.append(arg)
            continue

        # openai-whisper spells flags with underscores, mlx_whisper with hyphens.
        name, sep, value = arg.partition("=")
        name = name.replace("_", "-")
        flags.add(name)

        if name == "--model":
            if sep:
                value = MODEL_ALIASES.get(value, value)
            else:
                model_value_next = True
        out.append(name + sep + value)

    if "--model" not in flags:
        out += ["--model", MODEL_ALIASES[DEFAULT_MODEL]]
    if "--language" not in flags:
        out += ["--language", DEFAULT_LANGUAGE]
    return out


def main() -> None:
    sys.argv = [sys.argv[0], *translate_args(sys.argv[1:])]

    from mlx_whisper.cli import main as mlx_main

    mlx_main()


if __name__ == "__main__":
    main()
