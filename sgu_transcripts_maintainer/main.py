import sentry_sdk

from sgu_transcripts_maintainer.config import SENTRY_DSN

sentry_sdk.init(dsn=SENTRY_DSN, traces_sample_rate=1.0)


def main() -> None:
    """Main function."""


if __name__ == "__main__":
    main()
