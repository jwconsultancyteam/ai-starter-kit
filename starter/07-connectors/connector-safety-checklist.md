# Connector safety checklist

Use it for every connector you add, not only the calendar. Ten checks, about 5 minutes.

## Before you connect

- [ ] **Who made it?** The connector page on claude.ai says **Made by**. Only connect apps from developers you trust.
      Anthropic says it does not control which tools a developer makes available.
- [ ] **Which account?** Connect a test account first. Claude sees what that account can see.
- [ ] **Which tools?** Read the **Tools** list on the connector page. Sort them in two groups: tools that read, and
      tools that change, send or delete.

## Right after you connect

- [ ] **Tool permissions:** Customize > Connectors > the connector > **Tool permissions**.
      Reads on **Always allow**. Changes on **Needs approval**. Tools you never need on **Blocked**.
- [ ] **One chat at a time:** switch the connector on only in the chats that need it (**+** > **Connectors**).
- [ ] **Test run:** ask one question on the test account. Check the answer against the app itself.

## Every time Claude asks

- [ ] Read what the tool will do before you click.
- [ ] **Allow once** for anything that changes, sends or deletes.
- [ ] Never **Always allow** for a tool that changes things.

## When you stop using it

- [ ] **Disconnect** it under Customize > Connectors. Remove it from the list if you will not use it again.

---

Team and Enterprise plans: an Owner decides which connectors the organization can use, under Organization
settings > Connectors.

Sources: Claude docs [Get started with connectors](https://claude.com/docs/connectors/getting-started) and the
Google Calendar connector page on claude.ai, both read 18 Oct 2026.
