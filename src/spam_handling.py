# vim: set filetype=python tabstop=4 shiftwidth=4 expandtab:

import regex

_spam_checks = []


def spam_check(name="Missingno.", all=False, sites=set(), max_rep=10, max_score=1):
    def decorator(func):
        def check(post):
            if post.owner_rep <= max_rep and post.post_score <= max_score and all == (post.post_site not in sites):
                reason = func(post)

                if reason:
                    return True, "%s: %s" % (name, reason)
                else:
                    return False, ""
            else:
                return False, ""

        _spam_checks.append((name, check))
        return check

    return decorator


def regex_spam_check(re, name="Missingno.", all=False, sites=set(), max_rep=10, max_score=1, **types):
    compiled_regex = regex.compile(re)

    @spam_check(name=name, all=all, sites=sites, max_rep=max_rep, max_score=max_score)
    def check(post):
        reasons = []

        for key, value in types.items():
            if value:
                match = regex.search(compiled_regex, post[key])

                if match:
                    reasons.append("%s: %r" % (key, match))

        return ",".join(reasons)

    return check


def check_if_spam(post):
    reasons = []
    why = []

    for name, check in _spam_checks:
        result, reason = check(post)

        if result:
            reasons.append(name)
            why.append(reason)

    return reasons, why
