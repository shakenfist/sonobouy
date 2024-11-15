import time

from sonobouy import assertions_base


class HaveDnf(assertions_base.AssertionBase):
    internal_name = 'packages_have_dnf'
    pretty_name = 'Packages are managed by dnf or yum'

    def execute(self):
        try:
            import dnf.base
            return True
        except ModuleNotFoundError:
            return False


class DnfRecentlyUpdated(assertions_base.AssertionBase):
    internal_name = 'packages_dnf_recently_updated'
    pretty_name = 'Packages recently updated (dnf / yum)'
    depends_on = ['packages_have_dnf']

    def execute(self):
        import dnf.base

        b = dnf.base.Base()
        last_update = None
        for transaction in b.history.old():
            if transaction.cmdline.startswith('upgrade'):
                last_update = transaction.beg_timestamp

            # If we did not find an upgrade command, then the most recent
            # upgrade is just transaction zero when the instance image was
            # built.
            if not last_update:
                last_update = transaction.beg_timestamp

        # No transactions?
        if not last_update:
            return False

        if time.time() - last_update < 3600 * 24 * 14:
            return True
        return False


assertions_base.register(HaveDnf())
assertions_base.register(DnfRecentlyUpdated())
