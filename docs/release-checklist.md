# Release Checklist

## v0.3.0 manual release steps

1. Confirm `main` is clean and up to date.
2. Confirm package metadata reports `0.3.0`.
3. Run local validation.
4. Confirm CI passes on the release PR.
5. Merge the release PR.
6. Pull latest `main`.
7. Create an annotated tag:

   ```bash
   git tag -a v0.3.0 -m "v0.3.0"
   git push origin v0.3.0
   ```

8. Create a GitHub release from the tag using the `CHANGELOG.md` `0.3.0`
   section.
9. Do not publish to PyPI unless a separate package distribution issue
   explicitly adds that scope.
