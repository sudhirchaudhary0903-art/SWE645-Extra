# Demo Script

Use the AI Survey Assistant page at `/ai-assistant`.

## 1. Create Survey

Prompt:

```text
Create a survey for Jane Smith. She liked atmosphere and sports and heard from friends.
```

Expected behavior:

- Agent identifies create intent.
- Agent starts a draft.
- Agent asks for missing required fields.

Continue with:

```text
Her address is 4400 University Drive, Fairfax VA 22030. Phone is 703-555-0199. Email is jane.smith@example.com. Survey date is 2026-04-22. Recommendation is Very Likely.
```

Expected behavior:

- Agent summarizes the completed survey.
- Agent asks for confirmation.

Click `Yes` or type:

```text
yes
```

Expected behavior:

- Agent calls `create_survey`.
- Agent displays the created survey ID and details.

## 2. Read Query

Prompt:

```text
Show all surveys where students liked dorm rooms.
```

Expected behavior:

- Agent identifies read/search intent.
- Agent calls `search_surveys` with `liked_most=dorm_rooms`.
- Agent displays matching surveys.

Count example:

```text
How many students are unlikely to recommend the school?
```

Expected behavior:

- Agent searches by recommendation.
- Agent returns the count.

## 3. Update Request

Prompt:

```text
Change Jane Smith's recommendation to Likely.
```

Expected behavior:

- Agent identifies update intent.
- Agent searches for Jane Smith.
- Agent displays the matching survey and proposed change.
- Agent asks for confirmation.

Confirm:

```text
yes
```

Expected behavior:

- Agent calls `update_survey`.
- Agent displays the updated survey.

## 4. Delete With Confirmation

Prompt:

```text
Delete Jane Smith's survey.
```

Expected behavior:

- Agent identifies delete intent.
- Agent searches for Jane Smith.
- Agent displays survey details.
- Agent asks for confirmation.

Confirm:

```text
yes
```

Expected behavior:

- Agent calls `delete_survey`.
- Agent reports successful deletion.

## Deployment Proof

Capture this command in the video:

```bash
kubectl get pods -n portal-survey
```

Required pods to show:

- `portal-survey-ui`
- `portal-survey-agent`
- `portal-survey-api`

Also show:

```bash
kubectl get svc -n portal-survey
helm status portal-survey -n portal-survey
```

