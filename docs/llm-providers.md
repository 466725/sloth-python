# LLM Provider Configuration

This guide describes the supported ways to configure language-model providers
for DSA, the relevant environment variables, and ways to diagnose connection
problems. Provider availability, model names, account permissions, pricing, and
regional access can change; confirm current details in the provider console.
The provider presets in the Web settings UI are configuration references, not a
guarantee that a model is enabled for a particular account or endpoint.

For the exact dependency constraints, see [`requirements.txt`](../requirements.txt).
The repository currently pins LiteLLM below major version 2 and OpenAI SDK below
major version 3. Review and install dependencies as a compatible set rather
than upgrading either package independently.

## Choose a configuration method

| Method | Best for | Main settings |
| --- | --- | --- |
| Legacy provider variables | A simple single-provider setup | `LITELLM_MODEL` and the provider's existing API key |
| Channels | Multiple providers, multiple keys, or Web-based configuration | `LLM_CHANNELS` and `LLM_<CHANNEL>_*` |
| LiteLLM YAML | Advanced routing aliases or custom deployments | `LITELLM_CONFIG` and `LITELLM_MODEL` |

Configuration precedence is **YAML → Channels → legacy provider settings**.
YAML takes precedence only when its path can be read and it contains a usable
`model_list`; otherwise DSA falls back to the next configuration source. The
configuration loader does not rewrite or remove lower-priority settings.

Channels are the recommended option for most users and can be managed in the
Web app's **AI Model Configuration** settings. Use **Quick Add Channel** to
select a provider, enter its API key, optionally fetch models, select the
primary/Agent/fallback/vision models, save, and test the connection.

Runtime capability checks for JSON output, tools, streaming, or vision are
separate from the basic connection test. They must be explicitly triggered,
make real provider requests, and may incur cost or use account quota. Their
results describe one account/model/endpoint check, are best-effort, and do not
block saving the configuration.

## Configure Channels

Each channel has a name and may define a protocol, base URL, one or more API
keys, one or more model IDs, optional extra headers, and an enabled flag. The
`LLM_CHANNELS` value is a comma-separated list of channel names. For example:

```dotenv
LLM_CHANNELS=deepseek,gemini

LLM_DEEPSEEK_PROTOCOL=deepseek
LLM_DEEPSEEK_BASE_URL=https://api.deepseek.com
LLM_DEEPSEEK_API_KEY=replace-with-a-secret
LLM_DEEPSEEK_MODELS=deepseek-v4-flash,deepseek-v4-pro

LLM_GEMINI_PROTOCOL=gemini
LLM_GEMINI_API_KEYS=key-one,key-two
LLM_GEMINI_MODELS=gemini-3.1-pro-preview

LITELLM_MODEL=deepseek/deepseek-v4-flash
```

Use the provider's protocol for its native integration (`deepseek`, `gemini`,
`anthropic`, or `ollama`), and use `openai` for OpenAI-compatible endpoints.
For a custom OpenAI-compatible service:

```dotenv
LLM_CHANNELS=my_proxy
LLM_MY_PROXY_PROTOCOL=openai
LLM_MY_PROXY_BASE_URL=https://your-proxy.example.com/v1
LLM_MY_PROXY_API_KEY=replace-with-a-secret
LLM_MY_PROXY_MODELS=model-a,model-b
LITELLM_MODEL=openai/model-a
```

Keep API keys and headers containing credentials in a private `.env` file or
secret store; do not commit real values. A channel may use `LLM_<CHANNEL>_API_KEY`
or `LLM_<CHANNEL>_API_KEYS`. Set `LLM_<CHANNEL>_ENABLED=false` to skip a channel.
The local Ollama endpoint usually needs no API key; the host running DSA must be
able to reach the configured Ollama URL.

The [`.env.example` file](../.env.example) contains additional provider examples
for OpenAI, AIHubmix, Anspire Open, Moonshot/Kimi, DashScope, Zhipu, MiniMax,
MiMo, Volcengine, SiliconFlow, OpenRouter, and Ollama. Treat model IDs and
regional endpoints in those examples as starting points, and verify them with
the provider before use.

## Provider reference

The following examples reflect the repository's current environment templates.
They are not an exhaustive list of models or a compatibility certification.

| Provider / service | Channel | Protocol | Example base URL |
| --- | --- | --- | --- |
| OpenAI | `openai` | `openai` | `https://api.openai.com/v1` |
| AIHubmix | `aihubmix` | `openai` | `https://aihubmix.com/v1` |
| Anspire Open | `anspire` | `openai` | `https://open-gateway.anspire.cn/v6` |
| DeepSeek | `deepseek` | `deepseek` | `https://api.deepseek.com` |
| Google Gemini | `gemini` | `gemini` | Provider default; normally leave blank |
| Anthropic Claude | `anthropic` | `anthropic` | Provider default; normally leave blank |
| Moonshot / Kimi | `moonshot` | `openai` | `https://api.moonshot.cn/v1` |
| Alibaba DashScope | `dashscope` | `openai` | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| Zhipu GLM | `zhipu` | `openai` | `https://open.bigmodel.cn/api/paas/v4` |
| MiniMax | `minimax` | `openai` | `https://api.minimax.io/v1` |
| Xiaomi MiMo | `mimo` | `openai` | Use the endpoint from the provider console |
| Volcengine Ark / Doubao | `volcengine` | `openai` | `https://ark.cn-beijing.volces.com/api/v3` (region-specific) |
| SiliconFlow | `siliconflow` | `openai` | `https://api.siliconflow.cn/v1` |
| OpenRouter | `openrouter` | `openai` | `https://openrouter.ai/api/v1` |
| Ollama | `ollama` | `ollama` | `http://127.0.0.1:11434` |

Provider-specific model names and available endpoints change. Use the provider
documentation and account console as the source of truth. Useful references
include [LiteLLM providers](https://docs.litellm.ai/docs/providers),
[LiteLLM OpenAI-compatible providers](https://docs.litellm.ai/docs/providers/openai_compatible),
and the [LiteLLM YAML configuration reference](https://docs.litellm.ai/docs/proxy/configs).

## OpenAI-compatible model names and URLs

- Use `openai` as the channel protocol for a service that implements an
  OpenAI-compatible Chat Completions API.
- The model selected in `LITELLM_MODEL` generally uses the
  `openai/<provider-model-id>` form. For example, `Qwen/Model-X` as the
  provider's model ID is normally selected as `openai/Qwen/Model-X`; the
  provider/model ID itself is not a LiteLLM protocol name.
- Set the base URL to the compatible API root published by the provider, often
  ending in `/v1` or `/api/v3`. Do not append `/chat/completions` unless the
  provider's integration specifically requires it.
- For native LiteLLM providers, use their provider prefix (such as
  `gemini/model`, `anthropic/model`, or `deepseek/model`) and provider-specific
  settings.

For custom aliases, YAML `model_name` is the alias selected by
`LITELLM_MODEL`; `litellm_params.model` is the model identifier sent to the
provider. See the [YAML example](litellm_config.example.yaml) for a minimal
configuration. DSA parses the `model_list` from the YAML and creates its own
LiteLLM Router; LiteLLM Proxy server settings such as `router_settings` are not
read from the file.

## GitHub Actions

The repository's daily-analysis workflow is under
[`00-daily-analysis.yml`](../.github/workflows/disabled/00-daily-analysis.yml)
and is disabled; it is not an active scheduled deployment. It can be used as a
reference for environment mapping if you maintain a workflow of your own.
Workflows receive only variables explicitly mapped in their YAML. When using
Channels or a custom provider, map each required `LLM_<CHANNEL>_*` variable
yourself, and put API keys in GitHub Secrets rather than Variables.

The disabled workflow also supports `LITELLM_CONFIG_YAML`: it writes that YAML
content to the path specified by `LITELLM_CONFIG` before starting DSA. This is
workflow behavior; the application itself reads the YAML file named by
`LITELLM_CONFIG`.

An Ollama URL such as `127.0.0.1:11434` refers to the machine running the
backend. A GitHub-hosted runner will not normally have an Ollama service at that
address; use a reachable self-hosted service if needed.

## Troubleshooting

| Diagnostic / symptom | Common cause | What to check |
| --- | --- | --- |
| `missing_api_key` | No non-empty API key was resolved. | Check the provider key or channel key settings. Local Ollama may not require one. |
| `api_key_rejected` | Provider rejected the key or account. | Check key value, project/organization, model permissions, and regional restrictions. |
| `model_access_denied` or `model_not_found` | Model is disabled, unavailable to the account, or incorrectly named. | Check the exact model ID and account access in the provider console. |
| `insufficient_balance`, `quota_exceeded`, or `rate_limit` | Billing, quota, or request-rate limit. | Check account balance, project limits, RPM/TPM, and concurrency; retry after adjusting usage if appropriate. |
| `timeout`, `endpoint_not_found`, or `connection_refused` | Unreachable endpoint, incorrect path, or stopped local service. | Verify URL, port, provider-specific API root, firewall, and service availability. |
| `invalid_url` | URL contains a malformed or unsupported form. | Remove whitespace and credentials from the URL; use the documented base endpoint. |
| `provider_prefix_mismatch` | LiteLLM model prefix does not match the channel protocol. | Use `openai/<model>` for OpenAI-compatible channels or the correct native provider prefix. |
| `provider_blocked` | Provider or gateway policy denied the request. | Review the sanitized diagnostic, provider console, account status, region, and gateway policies. |
| `capability_unsupported` | The model or endpoint rejected a JSON, tool, stream, or vision check. | Treat it as a best-effort check for this model/account/endpoint; select a compatible model or endpoint. |

Diagnostic names are application classifications, not provider-standard error
codes. `model_access_denied` and `provider_blocked` use best-effort matching of
provider error text; inspect the test result and provider console before
concluding the cause. For the current implementation, see
[`ai_stock/services/system_config_service.py`](../ai_stock/services/system_config_service.py).

## Roll back configuration changes

- In Web settings, disable or remove the changed channel and restore the previous
  primary, Agent, fallback, or vision model.
- In `.env`, restore the previous `LLM_*`, `LITELLM_MODEL`,
  `AGENT_LITELLM_MODEL`, `VISION_MODEL`, and `LITELLM_FALLBACK_MODELS` values.
- To return from YAML to Channels or legacy configuration, unset
  `LITELLM_CONFIG` and restart the backend. To return from Channels to legacy
  settings, unset `LLM_CHANNELS`.
- Restore a previously exported system-configuration backup if one is available.

Configuration changes made for this guide require no database migration. If a
documentation change itself needs to be reverted, revert the documentation
change; runtime configuration and provider credentials are unaffected.
