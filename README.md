# mlx-whisper-cli

A `whisper` command for Apple Silicon Macs that takes the same arguments as OpenAI's `whisper` CLI but transcribes with [mlx-whisper](https://github.com/ml-explore/mlx-examples/tree/main/whisper), which runs on the Mac's GPU and is much faster.

```sh
whisper video.mp4 --model turbo --output_format txt
```

It is a thin wrapper: it rewrites the arguments and hands them to `mlx_whisper`.

- **Model names.** OpenAI short names (`turbo`, `large-v3`, `small.en`, ...) are mapped to the matching `mlx-community` repos on Hugging Face. A full repo name or a local path is passed through unchanged.
- **Flags.** Underscore flags such as `--output_format` are converted to the hyphenated form `mlx_whisper` expects. Either spelling works.
- **Defaults.** With no `--model` it uses `turbo`; with no `--language` it uses `en`.

## Requirements

- An Apple Silicon Mac
- [uv](https://docs.astral.sh/uv/)
- ffmpeg (`brew install ffmpeg`)

## Usage

Inside this folder, run it through uv:

```sh
uv run whisper ~/Downloads/meeting.mp4
```

The transcript is printed as it goes and saved as `meeting.txt` in the directory you run the command from, not next to the source file.

| Option | Effect |
|---|---|
| `--model large-v3` | Use a different model (default `turbo`) |
| `--language fr` | Transcribe another language (default `en`) |
| `--output_format srt` | `txt` (default), `vtt`, `srt`, `tsv`, `json` or `all` |
| `--output_dir ~/Downloads` | Save somewhere other than the current directory |
| `--output_name notes` | Name the output file `notes.txt` |
| `--verbose False` | Don't print the transcript to the terminal |

Run `whisper --help` for the full list.

The first run with a given model downloads it from Hugging Face into `~/.cache/huggingface` (about 1.6 GB for `turbo`). Later runs work offline. The "unauthenticated requests" warning during the download is harmless; no Hugging Face token is needed.

## Install globally

To use `whisper` from any directory, install it as a uv tool from this folder:

```sh
uv tool install --editable .
```

This puts a `whisper` command in `~/.local/bin`. Because the install is editable, changes to `src/whisper/__init__.py` take effect without reinstalling.

Two things to check:

1. **`~/.local/bin` is on your PATH.** If `which whisper` finds nothing in a new terminal, run `uv tool update-shell` and open another terminal.
2. **No other `whisper` is ahead of it.** If OpenAI's version is installed with Homebrew it will take priority, so remove it first:

   ```sh
   brew uninstall openai-whisper
   rm -rf ~/.cache/whisper   # optional: its downloaded models, which this tool can't use
   ```

`which whisper` should then print `~/.local/bin/whisper`.

To remove the global command: `uv tool uninstall mlx-whisper-cli`.

## License

MIT. See [LICENSE](LICENSE).
