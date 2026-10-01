# Fixing a Drupal edit form that crashes on a missing answer ID

## The problem

An editor opens an existing question to change its answers. Most questions work, but one edit form returns HTTP 500. The public page still loads. An empty or partially populated answer row reaches a custom field widget that assumes every row has an answer ID.

This is a realistic worked example of a missing-value defect in custom Drupal code. Names, logs and snippets below are synthetic; they are not a production incident transcript or evidence that these checks ran on a live site.

## Sample evidence

The custom widget passes a field value to a typed helper:

```php
$answer_id = $item->answer_id;
$title = $this->resolveAnswerTitle($answer_id);
```

The project's helper has this signature:

```php
private function resolveAnswerTitle(string $answer_id): string {
  // Project-specific lookup implementation.
}
```

A representative PHP error is:

```text
TypeError: ExampleAnswerWidget::resolveAnswerTitle():
Argument #1 ($answer_id) must be of type string, null given
```

The exact helper, field properties and exception wording will differ in your project. The error establishes that a null value reached a non-nullable parameter; it does not establish why the value is missing.

## Use the toolkit

Use the [Incident Debugger profile](../.github/agents/incident-debugger.agent.md) with the [log-analysis skill](../.agents/skills/drupal-log-analysis/SKILL.md). The [application-error prompt](../.github/prompts/investigate-application-error.prompt.md) is the entry point.

Copy this request into your coding assistant and supply redacted logs and the relevant widget source:

> Read AGENTS.md and .agents/skills/drupal-log-analysis/SKILL.md.
> Investigate an HTTP 500 when editing a question. The error reports a null
> answer ID passed to a typed helper in a custom field widget. Public viewing
> still works. Inspect the affected widget, field definition, stored-item
> handling and helper contract. Explain the supported cause and the next check.
> Do not change code or data yet.

Provide the environment, incident window/timezone, relevant deployed revision and reproduction steps when available. Do not include credentials, private URLs or personal content.

## What a useful investigation should establish

1. Locate the actual failing call using the stack trace and matching code revision.
2. Confirm the runtime value and field-item state on a disposable local example.
3. Inspect whether blank rows are valid during form construction, and whether saved data can contain incomplete items.
4. Distinguish an absent ID from a present ID whose referenced answer no longer exists.
5. Check whether the problem is limited to the edit widget or also affects validation, saving and display.

Do not conclude that a recent core upgrade caused the issue solely because the error appeared afterward. Do not delete content or clear caches as an automatic first fix.

## Example bounded fix

If the project's field contract permits null or an empty string while building the form, guard the lookup and provide the intended blank-row behavior:

```php
$answer_id = $item->answer_id;
$title = '';

if ($answer_id !== NULL && $answer_id !== '') {
  $title = $this->resolveAnswerTitle($answer_id);
}
```

This snippet assumes every non-null ID is already a string, as required by this project's helper. Verify that assumption against the field schema and data. Adapt the condition for a numeric-ID contract; do not blindly cast malformed values to strings.

An explicit condition preserves a valid string ID such as '0' if the project permits it. A blanket empty() check would also classify '0' as empty.

The guard prevents this particular invalid call. It does not repair orphaned references or prove incomplete saved answers are valid. Handle missing referenced records separately and enforce required-answer rules during validation if the business requirement demands them. Decide whether a blank title is appropriate for the actual widget before using this fix.

After reviewing the diagnosis, request implementation explicitly:

> Apply the smallest supported fix in the affected custom widget on the local
> development environment. Preserve valid-answer behavior and existing data.
> Verify missing, empty, valid and unresolved IDs using the project's checks.
> Report what ran and any remaining gaps. Do not deploy.

## Verification plan

These are checks to execute in the target project, not completed results:

| Case | Expected behavior |
| --- | --- |
| New question with an untouched answer row | Form builds without passing null to the helper |
| Existing question with an absent/empty ID | Form remains usable with the agreed blank-row behavior |
| Valid answer ID | Existing title and editing behavior remain intact |
| Present ID with no matching answer | Project-defined validation or fallback; no unrelated exception |
| Save and reopen valid answers | Values persist and display correctly |
| User without edit permission | Access remains denied |

Run the existing PHP/code-quality checks and an appropriate widget/form regression test when available. Record actual commands and results. Verify configuration/database impact separately; a widget guard alone does not require deleting or rewriting content.

## Why this example is useful

The same investigation pattern applies to optional entity references, incomplete Paragraph items, imported legacy data and other custom widgets: trace the failing contract, distinguish missing values from missing referenced records, fix only the supported failure, and verify both empty and valid inputs.
