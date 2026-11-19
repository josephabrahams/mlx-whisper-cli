"""`whisper` command that accepts openai-whisper style arguments and runs mlx-whisper."""

import os
import sys

DEFAULT_MODEL = "turbo"

# Set this to a language code (e.g. "en") to skip auto-detection by default.
LANGUAGE_ENV_VAR = "WHISPER_LANGUAGE"

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

# openai-whisper hardware flags that mean nothing on MLX. They are dropped,
# along with their value, so commands written for openai-whisper still run.
IGNORED_FLAGS = {"--device", "--fp16", "--threads"}


def translate_args(args: list[str], default_language: str | None = None) -> list[str]:
    """Rewrite openai-whisper style arguments into mlx_whisper ones."""
    out: list[str] = []
    flags: set[str] = set()
    pending: str | None = None  # "model" or "ignored": how to treat the next value

    for arg in args:
        if pending and not arg.startswith("--"):
            if pending == "model":
                out.append(MODEL_ALIASES.get(arg, arg))
            pending = None
            continue
        pending = None

        if not arg.startswith("--"):
            out.append(arg)
            continue

        # openai-whisper spells flags with underscores, mlx_whisper with hyphens.
        name, sep, value = arg.partition("=")
        name = name.replace("_", "-")

        if name in IGNORED_FLAGS:
            if not sep:
                pending = "ignored"
            continue

        flags.add(name)
        if name == "--model":
            if sep:
                value = MODEL_ALIASES.get(value, value)
            else:
                pending = "model"
        out.append(name + sep + value)

    if "--model" not in flags:
        out += ["--model", MODEL_ALIASES[DEFAULT_MODEL]]
    if "--language" not in flags and default_language:
        out += ["--language", default_language]
    return out


def main() -> None:
    args = translate_args(sys.argv[1:], os.environ.get(LANGUAGE_ENV_VAR))
    sys.argv = [sys.argv[0], *args]

    from mlx_whisper.cli import main as mlx_main  # type: ignore[import-untyped]

    mlx_main()


if __name__ == "__main__":
    main()
