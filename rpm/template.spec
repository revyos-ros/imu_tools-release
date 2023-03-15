%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-imu-filter-madgwick
Version:        2.1.3
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS imu_filter_madgwick package

License:        GPL
URL:            http://ros.org/wiki/imu_filter_madgwick
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-rolling-builtin-interfaces
Requires:       ros-rolling-geometry-msgs
Requires:       ros-rolling-nav-msgs
Requires:       ros-rolling-rclcpp
Requires:       ros-rolling-rclcpp-action
Requires:       ros-rolling-rclcpp-lifecycle
Requires:       ros-rolling-sensor-msgs
Requires:       ros-rolling-tf2-geometry-msgs
Requires:       ros-rolling-tf2-ros
Requires:       ros-rolling-visualization-msgs
Requires:       ros-rolling-ros-workspace
BuildRequires:  ros-rolling-ament-cmake
BuildRequires:  ros-rolling-builtin-interfaces
BuildRequires:  ros-rolling-geometry-msgs
BuildRequires:  ros-rolling-nav-msgs
BuildRequires:  ros-rolling-rclcpp
BuildRequires:  ros-rolling-rclcpp-action
BuildRequires:  ros-rolling-rclcpp-lifecycle
BuildRequires:  ros-rolling-sensor-msgs
BuildRequires:  ros-rolling-tf2-geometry-msgs
BuildRequires:  ros-rolling-tf2-ros
BuildRequires:  ros-rolling-visualization-msgs
BuildRequires:  ros-rolling-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-rolling-ament-cmake-gtest
%endif

%description
Filter which fuses angular velocities, accelerations, and (optionally) magnetic
readings from a generic IMU device into an orientation. Based on code by
Sebastian Madgwick,
http://www.x-io.co.uk/node/8#open_source_ahrs_and_imu_algorithms.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/rolling

%changelog
* Wed Mar 15 2023 Martin Günther <martin.guenther@dfki.de> - 2.1.3-1
- Autogenerated by Bloom

