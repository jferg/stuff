# from solution.quantity import Quantity

class Quantity(object):
    """
    Represents dimensional quantities, i.e. quantities with units, and implements
    arithmetic on them. Useful for verifying that a calculation sanity-checks;
    basically static typing but for applied math. Mostly associated with physics and
    chemistry, but can be applied to finance, operations and logistics,
    or just about anything else quantitative.
    """

    def __init__(self, units, magnitude=None):
        pass


q = Quantity


def test_arithmetic():
    """
    We should be able to add and subtract quantities (at least, if they have the same units).
    """

    total_users = q('users', 1e4)
    premium_users = q('users', 7e2)
    standard_users = total_users - premium_users
    recalculated_total = standard_users + premium_users
    are_equal = total_users == recalculated_total
    print '{total_users} == {recalculated_total} is {are_equal}'.format(**locals())


def test_multiply():
    """
    When we multiply two quantities together, their units need to "combine";
    for each dimension of each quantity, the resulting quantity's units should
    have the *sum* of the powers of that unit for all quantities.

    (If a unit is missing from a given quantity, its power is 0; likewise,
    if the power of a unit in a quantity resulting from some operation is 0,
    that unit should be removed from that quantity's units completely.)
    """

    visible_area = q('pixels', 750 * 160)
    visible_time = q('seconds', 4.7)
    total_viewability = visible_area * visible_time
    print '\nmultiplication:'
    print '{visible_area} * {visible_time} = {total_viewability}'.format(**locals())
    # (something similar to) 5.64e+05 pixels * seconds


def test_power():
    """
    Raising dimensional quantities to integer powers is allowed.
    (and non-integer powers, in some cases, but don't worry about that.)
    The powers of each unit should be multiplied by the given exponent.
    """

    cycle_time = q('seconds', 4.2 * 10**-10)
    hz_conversion = q('seconds') * q('hertz')
    frequency = cycle_time**-1 * hz_conversion
    print '\nexponentiation:'
    print '({cycle_time})^-1 = {frequency}'.format(**locals())
    # 2.38e+09 * hertz


def test_divide():
    """
    Division is almost identical to multiplication...
    """
    requests_per_day = q('requests', 10**6) / q('day')
    users_per_day = q('users', 3 * 10**4) / q('day')
    requests_per_user = requests_per_day / users_per_day
    print '\ndivision:'
    print '{requests_per_day} / {users_per_day} = {requests_per_user}'.format(**locals())
    # 33.33 requests * user^-1


def test_usability():
    """
    The specific contents of this test aren't very important (though they might
    be interesting); this doesn't add any new functionality not covered by the
    other tests, it just verifies that we can multiply and divide a lot of quantities
    where many units end up canceled out and still get a user-friendly result.
    """

    # we want to scrape a certain number of sites at a certain rate;
    # how much computing power do we need to handle that?
    scrapes_per_site = 10 * q('scrape') / q('site')
    sites_per_day = 5000 * q('site') / q('day')
    scrapes_per_day = scrapes_per_site * sites_per_day

    # assume each scrape has some processing that we're going to do
    # synchronously, so we're CPU bound; how much CPU do we need?
    core_seconds_per_scrape = 15 * q('core') * q('second') / q('scrape')
    core_time_per_day = scrapes_per_day * core_seconds_per_scrape
    seconds_per_day = 86000 * q('second') / q('day')
    cores_needed = core_time_per_day / seconds_per_day

    # and how many "c3.xlarge" (quad-core) EC2 instances does that correspond to?
    cores_per_instance = 4 * q('core') / q('c3.xlarge')
    instances_needed = cores_needed / cores_per_instance
    import math
    instances_deployed = math.ceil(instances_needed.magnitude) * q(instances_needed.units)
    utilization = instances_needed / instances_deployed

    print '\nusability:'
    print ('need {cores_needed} (= {instances_deployed})'
           ' for {scrapes_per_day} (utilization: {utilization})').format(**locals())


test_arithmetic()
test_multiply()
test_power()
test_divide()
test_usability()
