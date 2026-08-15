# LoadRunner Best Practices for Beginners

This guide is meant to help beginners create simple, reliable, and useful performance tests with LoadRunner.

The goal is not to make the test "heavy" or complicated. A good performance test is easy to understand, stable, and realistic.

---

## 1. Start with a clear testing goal

Before recording or scripting, ask:

- What is the business action being tested?
- Which page or API is most important?
- How many users should be simulated?
- What response time is acceptable?

Examples:

- Login page response time under 2 seconds
- Search feature handles 100 virtual users
- Checkout workflow stays stable under 50 concurrent users

A test without a goal is hard to trust.

---

## 2. Keep the test close to real user behavior

Performance tests should model realistic user actions.

Good practice:

- Use real workflows, not random clicks
- Test common user journeys like login, search, checkout, and logout
- Keep the script aligned with production behavior
- Use realistic data and realistic timing

Avoid:

- Clicking UI elements in an unrealistic order
- Creating scripts that do too much in one transaction
- Reusing the same data in a way that causes unrealistic lockups or duplicate actions

---

## 3. Learn the difference between a transaction and a step

A transaction is a logical action such as:

- Login
- Search
- Add to cart
- Submit order

A step is one part of the flow, such as:

- Open login page
- Enter username
- Click login
- Wait for homepage

Use transactions for measuring business performance and use steps for debugging.

Best practice:

- Start transactions only around real user actions
- Keep transaction names clear and business-friendly
- Avoid too many small transactions that make reporting noisy

---

## 4. Use realistic think time

Think time is the pause between actions that simulates a real user reading or deciding.

If you remove think time completely, the test may become too aggressive and unrealistic.

Good approach:

- Use natural pauses between actions
- Keep some variation in delay rather than a fixed value everywhere
- Add think time only where the user would naturally pause

Example:

- Search page: 2 to 5 seconds
- Login page: 1 to 3 seconds
- Form filling: small but realistic delay

Too little think time can create unrealistic load. Too much think time may hide actual bottlenecks.

---

## 5. Correlate dynamic values correctly

Many applications generate values such as:

- session IDs
- tokens
- request IDs
- hidden form values
- dynamic parameters in URLs

If these values are not correlated correctly, the script will fail under load.

Best practices:

- Capture values from server responses
- Save them in parameter variables
- Use the saved values in later requests

Common examples:

- CSRF token
- JSESSIONID
- payment token
- hidden field values

If a script fails with errors like "invalid session" or "token mismatch," correlation is often the issue.

---

## 6. Parameterize test data

Do not use the same username or same data for every user unless the scenario requires it.

Use parameterization for:

- usernames
- passwords
- product IDs
- search terms
- customer numbers

Benefits:

- More realistic load
- Better test coverage
- Reduced chance of hitting cache or duplicate behavior by accident

Keep data files clean and controlled. A small, valid dataset is better than a huge, confusing one.

---

## 7. Design the workload carefully

The load profile matters as much as the script itself.

Start with:

- 1 user: basic script validation
- 5 to 10 users: checks for logic and stability
- then more users gradually: ramp up to target load

Use a ramp-up pattern to avoid sudden spikes that hide the actual bottleneck.

Example:

- Ramp up: 10 users every 30 seconds
- Hold: run at target load for a fixed period
- Ramp down: reduce users gradually

This helps you observe how the system behaves under increasing pressure.

---

## 8. Keep a small, stable script first

Begin with the simplest version of the scenario.

Good beginner flow:

1. Record one transaction
2. Run it once manually
3. Fix any script errors
4. Add correlation and think time
5. Run with a few users
6. Increase load slowly

Do not start with a huge and complex script. Complex scripts are harder to debug and easier to break.

---

## 9. Validate the script before running large loads

Before increasing user load, check that the script:

- runs successfully with a single user
- logs in correctly
- handles authentication and tokens
- returns expected pages or responses
- contains all required input values

If the script is not valid at low load, it will not become valid at high load.

---

## 10. Monitor the system while the test runs

LoadRunner is not only about script success. You also need system health.

Monitor:

- CPU usage
- memory usage
- disk I/O
- network latency
- application response time
- database performance
- web server health

You want to answer: "Did the app slow down because of user load, or because of server-side bottlenecks?"

If the app fails only under load, the system bottleneck is usually visible in the monitor data.

---

## 11. Separate test results from script errors

A failed script can mean different things:

- application bug
- incorrect correlation
- server response changed
- wrong path or missing parameter
- test setup problem

Always inspect the response and logs before assuming the system is slow.

A script that fails to complete is not a valid performance result.

---

## 12. Use naming conventions that are easy to read

Clear naming helps beginners and teams stay consistent.

Good examples:

- Login_01
- Search_Product
- Add_To_Cart
- Checkout_Complete

Avoid names like:

- Action1
- Test_ABC
- Step_123
- RandomFlow

Clear names make troubleshooting much easier.

---

## 13. Keep tests maintainable

A performance test should be easy to update when the application changes.

Best practices:

- Avoid hardcoded values when parameters are possible
- Reuse common actions when appropriate
- Keep scripts readable
- Document assumptions and test setup
- Store important data separately from the script logic

If a script is hard to read, it will be hard to maintain.

---

## 14. Avoid over-optimizing too early

Beginners often try to make a script look perfect before testing it.

Better approach:

- make script work
- run with small load
- confirm behavior
- improve realism step by step

This keeps the project moving and helps catch issues early.

---

## 15. Keep an eye on errors and warnings

Watch for patterns such as:

- HTTP 500 errors
- timeout errors
- login failures
- token errors
- session invalidation
- missing response content

These are often better clues than raw latency numbers alone.

A system can look fast in some reports while still failing important user actions.

---

## 16. Focus on business-critical scenarios first

Do not start by testing everything at once.

Prioritize:

- login flow
- search flow
- checkout
- payment submission
- high-traffic pages

Begin with the critical path that matters most to users.

Once that works reliably, expand to secondary flows.

---

## 17. Use a simple validation checklist

Before each test run, check:

- Script runs successfully with one user
- Correlation is working
- Think time is realistic
- Data is parameterized
- Transaction names are clear
- System monitors are enabled
- Expected result is known

If you cannot explain the expected behavior, the test is not ready.

---

## 18. Common beginner mistakes to avoid

Here are the most common problems:

- Running large load without checking the script at low load
- Removing all think time
- Forgetting to correlate dynamic values
- Using one static user for all virtual users
- Measuring only response time and ignoring errors
- Not monitoring server health
- Script complexity growing faster than understanding

Avoid these and your tests will be much more stable.

---

## 19. A simple beginner workflow

A practical workflow for new LoadRunner users:

1. Define the user flow to test
2. Record a simple script
3. Validate it with one virtual user
4. Add correlation and valid data
5. Add realistic think time
6. Run a small load test
7. Review errors and response times
8. Increase users gradually
9. Monitor server resources
10. Compare results to your target goal

This makes performance testing easier to learn and easier to trust.

---

## 20. Final rule: test for realism, not just numbers

A performance test is useful only when it reflects real usage.

Good performance testing is not about creating the biggest possible load. It is about:

- testing realistic user flows
- measuring real bottlenecks
- catching issues before users do
- producing repeatable and understandable results

If your script is clear, stable, and realistic, you are already following the right path.

---

## Quick beginner checklist

Use this list before every test run:

- [ ] I know the business action being tested
- [ ] The script is valid with 1 user
- [ ] Correlation is in place
- [ ] Think time looks realistic
- [ ] Test data is parameterized
- [ ] Transaction names are clear
- [ ] System monitors are ready
- [ ] I know the expected outcome
- [ ] I will increase load gradually

---

## Recommended mindset

Think of LoadRunner as a tool for learning how the system behaves under pressure, not just a way to generate numbers.

The best performance tests are simple, realistic, and easy to explain.
