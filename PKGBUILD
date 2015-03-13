# Contributor: Charles Leifer
# Maintainer: Sol Bekic <s0lll0s at blinkenshell dot org>

_gitname=themer
_gitbranch=master
pkgname="python-${_gitname}-git"
pkgdesc='Themer is a colorscheme generator and manager for your desktop.'
pkgver=0.4
pkgrel=1
url="https://github.com/s0lll0s/${_gitname}"
license=('MIT')
arch=('any')
depends=('python>=3.2' 'python-pillow' 'python-yaml' 'python-jinja')
optdepends=('i3: default-supported windowmanager' 'fish')
makedepends=('git' 'python-setuptools')
conflicts=()
install="${_gitname}.install"
source=("${_gitname}::git://github.com/s0lll0s/${_gitname}.git#branch=${_gitbranch}"
        "${install}")
sha256sums=('SKIP'
            '3b15c5f5102135a377299ba4dd38ed7b9f71ac0e1d27fc96d9be2105a1b34125')

pkgver() {
  cd "${_gitname}"
  echo "$(git rev-list --count ${_gitbranch}).$(git rev-parse --short ${_gitbranch})"
}

package() {
  cd "${_gitname}"
  python setup.py install --root="${pkgdir}" --optimize=1

  install -Dm644 -d "${pkgdir}/usr/share/${_gitname}"
  cp -dr --no-preserve=ownership "data/default" "${pkgdir}/usr/share/${_gitname}"
  chmod -R 755 "${pkgdir}/usr/share/${_gitname}"
  install -Dm644 "LICENSE" "${pkgdir}/usr/share/licenses/${pkgname}/LICENSE"
  install -Dm644 "data/fish/themer.fish" "${pkgdir}/usr/share/fish/completitions/"
}
