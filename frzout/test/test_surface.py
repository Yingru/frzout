# -*- coding: utf-8 -*-

import numpy as np

from nose.tools import assert_almost_equal, assert_warns, assert_raises

from .. import Surface


def test_surface():
    volume = np.random.uniform(10, 100)
    tau = np.random.uniform(.5, 5.)

    x = np.atleast_2d([tau, 0., 0.])
    sigma = np.atleast_2d([volume/tau, 0., 0.])
    v = np.zeros((1, 2))

    surf = Surface(x, sigma, v)

    assert surf.boost_invariant, 'Surface should be boost-invariant.'

    assert_almost_equal(
        surf.volume, volume, delta=1e-12,
        msg='incorrect volume'
    )

    ymax = np.random.uniform(.5, 2.)
    surf = Surface(x, sigma, v, ymax=ymax)

    assert_almost_equal(
        surf.volume, 2*ymax*volume, delta=1e-12,
        msg='incorrect volume'
    )

    x = np.random.uniform(0, 10, size=(1, 4))
    sigma = np.random.uniform(0, 10, size=(1, 4))
    v = np.random.uniform(-.5, .5, size=(1, 3))

    surf = Surface(x, sigma, v)

    assert not surf.boost_invariant, 'Surface should not be boost-invariant.'

    gamma = 1/np.sqrt(1 - (v*v).sum())
    u_ = np.empty(4)
    u_[0] = gamma
    u_[1:] = -gamma*v

    volume = np.inner(sigma, u_)

    assert_almost_equal(
        surf.volume, volume, delta=1e-12,
        msg='incorrect volume'
    )

    with assert_warns(Warning):
        Surface(x, sigma, v, ymax=1.)

    with assert_raises(ValueError):
        Surface(
            np.ones((1, 1)),
            np.ones((1, 1)),
            np.ones((1, 1)),
        )

    with assert_raises(ValueError):
        Surface(
            np.ones((1, 4)),
            np.ones((1, 3)),
            np.ones((1, 2)),
        )

    with assert_raises(ValueError):
        Surface(
            np.ones((2, 4)),
            np.ones((2, 4)),
            np.ones((3, 3)),
        )