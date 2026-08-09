# Security Policy

## Secrets and credentials

Never commit:

- Hugging Face tokens
- Kaggle credentials
- API keys
- Employer, customer, or production evidence
- Real credentials, logs, or audit materials

Use environment variables or platform secret stores for GPU notebooks.

## Synthetic data only

The ControlSift benchmark is synthetic. Do not introduce real organizational evidence into the repository.

## Reporting

If you discover a security issue in this repository (for example, accidental credential exposure), open a private security advisory or contact the maintainers without posting secrets publicly.

## Intended use

ControlSift is research software for evaluating evidence-classification models. It is not an automated auditor, compliance engine, or production GRC product.
