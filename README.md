# mlx-whisper-cli

A `whisper` command for Apple Silicon Macs that takes the same arguments as OpenAI's `whisper` CLI but transcribes with [mlx-whisper](https://github.com/ml-explore/mlx-examples/tree/main/whisper), which runs on the Mac's GPU and is much faster.

```sh
whisper video.mp4 --model turbo --output_format txt
```

It is a thin wrapper: it rewrites the arguments and hands them to `mlx_whisper`.

- **Model names.** OpenAI short names (`turbo`, `large-v3`, `small.en`, ...) are mapped to the matching `mlx-community` repos on Hugging Face. A full repo name or a local path is passed through unchanged.
- **Flags.** Underscore flags such as `--output_format` are converted to the hyphenated form `mlx_whisper` expects. Either spelling works.
- **Hardware flags.** `--device`, `--fp16` and `--threads` mean nothing on MLX, so they are ignored instead of causing an error.
- **Defaults.** With no `--model` it uses `turbo`. With no `--language` the language is auto-detected, unless `WHISPER_LANGUAGE` is set.

## Requirements

- An Apple Silicon Mac
- [uv](https://docs.astral.sh/uv/)
- ffmpeg (`brew install ffmpeg`)

## Install

```sh
uv tool install git+https://github.com/josephabrahams/mlx-whisper-cli
```

This puts a `whisper` command in `~/.local/bin`. Two things to check:

1. **`~/.local/bin` is on your PATH.** If `which whisper` finds nothing in a new terminal, run `uv tool update-shell` and open another terminal.
2. **No other `whisper` is ahead of it.** If OpenAI's version is installed with Homebrew it will take priority, so remove it first:

   ```sh
   brew uninstall openai-whisper
   rm -rf ~/.cache/whisper   # optional: its downloaded models, which this tool can't use
   ```

`which whisper` should then print `~/.local/bin/whisper`.

To remove it: `uv tool uninstall mlx-whisper-cli`.

## Usage

```sh
whisper ~/Downloads/meeting.mp4
```

The transcript is printed as it goes and saved as `meeting.txt` in the directory you run the command from, not next to the source file.

| Option | Effect |
|---|---|
| `--model large-v3` | Use a different model (default `turbo`) |
| `--language en` | Set the language instead of auto-detecting it |
| `--output_format srt` | `txt` (default), `vtt`, `srt`, `tsv`, `json` or `all` |
| `--output_dir ~/Downloads` | Save somewhere other than the current directory |
| `--output_name notes` | Name the output file `notes.txt` |
| `--verbose False` | Don't print the transcript to the terminal |

Run `whisper --help` for the full list.

To always use one language without passing `--language`, set `WHISPER_LANGUAGE` in your shell profile:

```sh
export WHISPER_LANGUAGE=en
```

An explicit `--language` still overrides it.

The first run with a given model downloads it from Hugging Face into `~/.cache/huggingface` (about 1.6 GB for `turbo`). Later runs work offline. The "unauthenticated requests" warning during the download is harmless; no Hugging Face token is needed.

## Differences from OpenAI's whisper

- **Output format.** The default is `txt` only. OpenAI's CLI writes every format; pass `--output_format all` for that.
- **Unsupported flags.** `--beam_size`, `--model_dir` and `--temperature_increment_on_fallback` have no `mlx_whisper` equivalent and cause an "unrecognized arguments" error.
- **Ignored flags.** `--device`, `--fp16` and `--threads` are accepted and dropped.
- **Help text.** `whisper --help` shows `mlx_whisper`'s own help, with hyphenated flag names.

## Development

Clone the repo, then run the command and the tests through uv:

```sh
uv run whisper ~/Downloads/meeting.mp4
uv run pytest
```

To make your working copy the global `whisper`, install it in editable mode, so changes to `src/whisper/__init__.py` take effect without reinstalling:

```sh
uv tool install --editable .
```

## License

MIT. See [LICENSE](LICENSE).
