# Performance Testing Guide

This guide describes the performance and API testing assets currently stored in
`tests/performance/`. They are standalone tools and are not run by pytest or the
repository's standard `just verify` workflow.

## Repository assets

| Tool       | Asset                                                                                                                                                                                                                                                                                          | Purpose                                                                                                                                            |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| JMeter     | [`jmeter/theatre_movie_showtime_test.jmx`](jmeter/theatre_movie_showtime_test.jmx)                                                                                                                                                                                                             | netflix UAT theatre, movie, and showtime API workflow.                                                                                             |
| Locust     | [`locust/theatre_movie_showtime_test.py`](locust/theatre_movie_showtime_test.py)                                                                                                                                                                                                               | Python version of the same netflix workflow, with credentials and test inputs supplied through environment variables.                              |
| Postman    | [`postman/Daily regression test suite.postman_collection.json`](postman/Daily%20regression%20test%20suite.postman_collection.json), [`UAT.postman_environment.json`](postman/UAT.postman_environment.json), and [`Staging.postman_environment.json`](postman/Staging.postman_environment.json) | netflix API regression checks. This is a functional API collection, not a load generator.                                                          |
| LoadRunner | [`load_runner/`](load_runner/)                                                                                                                                                                                                                                                                 | Recorded Tangerine homepage and personal-login browser scenarios. Review and validate recordings before treating them as representative workloads. |

Use the tool that matches the goal: Postman for API behavior checks, or JMeter
and Locust to generate load against an explicitly authorized test system.

## netflix theatre/movie/showtime workflow

The JMeter and Locust scripts exercise this sequence:

1. Request the theatres list.
2. Request English-language movies.
3. Request theatres with showtimes for a film ID.
4. Extract `nearbyTheatres[*].theatreId` and request showtimes for each theatre
   and date.

The JMeter plan is configured for one thread, a one-second ramp-up, one loop,
and a 60-second thread-group duration. It also has a 100 ms constant timer. The
Locust user applies a 100 ms wait between requests and repeats the workflow for
the duration of the Locust run; it does not reproduce JMeter's one-loop limit.

The JMeter plan references `film_id`, which must be supplied when running it.
Its showtime date is fixed in the plan. The Locust script uses the same default
date but allows it and the API host to be overridden.

### Run the Locust scenario

Locust is not included in the repository's Python dependencies. Install it in
an appropriate isolated environment, then set the required variables in
PowerShell:

```powershell
python -m pip install locust
$env:netflix_SESSION_TOKEN = "<session-token>"
$env:netflix_SUBSCRIPTION_KEY = "<subscription-key>"
$env:netflix_FILM_ID = "<film-id>"
python -m locust -f tests/performance/locust/theatre_movie_showtime_test.py --headless --users 1 --spawn-rate 1 --run-time 60s
```

The script requires `netflix_SESSION_TOKEN`, `netflix_SUBSCRIPTION_KEY`, and
`netflix_FILM_ID`. Optional variables are:

| Variable                | Default                    | Purpose                                       |
| ----------------------- | -------------------------- | --------------------------------------------- |
| `netflix_API_HOST`      | `https://apis.netflix.com` | API host; the script uses the UAT API paths.  |
| `netflix_SHOWTIME_DATE` | `2022-03-02`               | Date sent with each theatre showtime request. |

Omit `--headless` to use Locust's web UI. Keep user count and run duration low
for an initial validation; agree on limits and obtain authorization before
increasing traffic. The current example targets an external netflix API, so do
not run a load test against it without the service owner's approval.

### JMeter notes

Open the JMX file in JMeter 5.6.3 or a compatible version. Configure `film_id`
and valid credentials for the intended environment before running it. The JMX
currently contains inline authentication values: do not share or reuse those
values as-is; replace them with securely supplied test credentials, and rotate
them if they are still active.

## Postman API regression collection

The `Daily regression test suite` collection groups requests under Login,
Movies, Theatres, and Showtimes. Its scripts check response values and carry
session tokens between requests. The UAT and Staging environment files supply
environment configuration. Use the collection to validate API behavior before
a performance run; repeated collection execution is not a substitute for a
load-testing tool.

Treat environment variables, credentials, and generated session tokens as
secrets. Keep real credentials out of exported collections and committed
environment files.

## LoadRunner recordings

The two recorded scenarios are under `load_runner/tangerine_homepage/` and
`load_runner/tangerine_personal_login/`. Their `Action.c` files contain
browser-recorded requests, including analytics, browser background traffic,
and third-party requests. These captures are not automatically clean or
representative load scripts: inspect the target requests, correlation, cookies,
and transaction boundaries before replaying or using results.

Recordings can include session cookies, identifiers, and browser-specific
metadata. Sanitize those values before sharing the scripts, and use only
approved test accounts and systems.

## Preparing and reviewing a run

Before generating load:

1. Confirm written authorization, target environment, allowed request rate,
   duration, and stop conditions.
2. Verify credentials and required test data using a single-user functional
   run. Never put secrets in command history, source files, or test reports.
3. Confirm each request uses the expected host, path, parameters, and dynamic
   values; check errors and response content, not only latency.
4. Choose user count, ramp-up, and duration based on an agreed workload model.
   The sample settings in these assets are examples, not capacity targets or
   service-level objectives.
5. Monitor the application and its dependencies during the run, and stop if
   error rates, resource use, or service-owner limits are exceeded.
6. Record the tool/version, target environment, workload settings, test-data
   source, timestamps, errors, and latency percentiles with the results.

Keep functional validation separate from performance measurement. A run with
invalid authentication, stale data, or unexpected request failures does not
provide a useful capacity result.
