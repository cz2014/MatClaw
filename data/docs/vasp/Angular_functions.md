# Angular functions

:   real spherical harmonics

    | *l* | *m* | Name | *Ylm* |
    | --- | --- | --- | --- |
    |  |  |  |  |
    | 0 | 1 | s | $\frac{1}{\sqrt{4\pi}}$ |
    |  |  |  |  |
    | 1 | -1 | py | $\sqrt{\frac{3}{4\pi}}\frac{y}{r}$ |
    | 1 | 0 | pz | $\sqrt{\frac{3}{4\pi}}\frac{z}{r}$ |
    | 1 | 1 | px | $\sqrt{\frac{3}{4\pi}}\frac{x}{r}$ |
    |  |  |  |  |
    | 2 | -2 | dxy | $\frac{1}{2}\sqrt{\frac{15}{\pi}}\frac{xy}{r^2}$ |
    | 2 | -1 | dyz | $\frac{1}{2}\sqrt{\frac{15}{\pi}}\frac{yz}{r^2}$ |
    | 2 | 0 | dz2 | $\frac{1}{4}\sqrt{\frac{5}{\pi}}\frac{3z^2-r^2}{r^2}$ |
    | 2 | 1 | dxz | $\frac{1}{2}\sqrt{\frac{15}{\pi}}\frac{zx}{r^2}$ |
    | 2 | 2 | dx2-y2 | $\frac{1}{4}\sqrt{\frac{15}{\pi}}\frac{x^2-y^2}{r^2}$ |
    |  |  |  |  |
    | 3 | -3 | fy(3x2-y2) | $\frac{1}{4}\sqrt{\frac{35}{2\pi}}\frac{(3x^2-y^2)y}{r^3}$ |
    | 3 | -2 | fxyz | $\frac{1}{2}\sqrt{\frac{105}{\pi}}\frac{xyz}{r^3}$ |
    | 3 | -1 | fyz2 | $\frac{1}{4}\sqrt{\frac{21}{2\pi}}\frac{(5z^2-r^2)y}{r^3}$ |
    | 3 | 0 | fz3 | $\frac{1}{4}\sqrt{\frac{7}{\pi}}\frac{(5z^2-3r^2)z}{r^3}$ |
    | 3 | 1 | fxz2 | $\frac{1}{4}\sqrt{\frac{21}{2\pi}}\frac{(5z^2-r^2)x}{r^3}$ |
    | 3 | 2 | fz(x2-y2) | $\frac{1}{4}\sqrt{\frac{105}{\pi}}\frac{(x^2-y^2)z}{r^3}$ |
    | 3 | 3 | fx(x2-3y2) | $\frac{1}{4}\sqrt{\frac{35}{2\pi}}\frac{(x^2-3y^2)x}{r^3}$ |

:   hybrid angular functions

    |  |  |  |
    | --- | --- | --- |
    | sp | sp-1 | $\frac{1}{\sqrt 2}\rm s+\frac{1}{\sqrt 2}\rm p\_x$ |
    |  |  |  |  |
    |  | sp-2 | $\frac{1}{\sqrt 2}\rm s-\frac{1}{\sqrt 2}\rm p\_x$ |
    |  |  |  |  |
    | sp2 | sp2-1 | $\frac{1}{\sqrt 3}\rm s-\frac{1}{\sqrt 6}\rm p\_x+\frac{1}{\sqrt 2}\rm p\_y$ |
    |  | sp2-2 | $\frac{1}{\sqrt 3}\rm s-\frac{1}{\sqrt 6}\rm p\_x-\frac{1}{\sqrt 2}\rm p\_y$ |
    |  | sp2-2 | $\frac{1}{\sqrt 3}\rm s+\frac{2}{\sqrt 6}\rm p\_x$ |
    |  |  |  |  |
    | sp3 | sp3-1 | $\frac{1}{2}(\rm s+\rm p\_x+\rm p\_y+\rm p\_z)$ |
    |  | sp3-2 | $\frac{1}{2}(\rm s+\rm p\_x-\rm p\_y-\rm p\_z)$ |
    |  | sp3-2 | $\frac{1}{2}(\rm s-\rm p\_x+\rm p\_y-\rm p\_z)$ |
    |  | sp3-4 | $\frac{1}{2}(\rm s-\rm p\_x-\rm p\_y+\rm p\_z)$ |
    |  |  |  |  |
    | sp3d | sp3d-1 | $\frac{1}{\sqrt 3}\rm s-\frac{1}{\sqrt 6}\rm p\_x+\frac{1}{\sqrt 2}\rm p\_y$ |
    |  | sp3d-2 | $\frac{1}{\sqrt 3}\rm s-\frac{1}{\sqrt 6}\rm p\_x-\frac{1}{\sqrt 2}\rm p\_y$ |
    |  | sp3d-3 | $\frac{1}{\sqrt 3}\rm s+\frac{2}{\sqrt 6}\rm p\_x$ |
    |  | sp3d-4 | $\frac{1}{\sqrt 2}\rm p\_z+\frac{1}{\sqrt 2}\rm d\_{z^2}$ |
    |  | sp3d-5 | $-\frac{1}{\sqrt 2}\rm p\_z+\frac{2}{\sqrt 2}\rm d\_{z^2}$ |
    |  |  |  |  |
    | sp3d2 | sp3d2-1 | $\frac{1}{\sqrt 6}\rm s-\frac{1}{\sqrt 2}\rm p\_x-\frac{1}{\sqrt 12}\rm d\_{z^2}+\frac{1}{2}\rm d\_{x^2-y^2}$ |
    |  | sp3d2-2 | $\frac{1}{\sqrt 6}\rm s+\frac{1}{\sqrt 2}\rm p\_x-\frac{1}{\sqrt 12}\rm d\_{z^2}+\frac{1}{2}\rm d\_{x^2-y^2}$ |
    |  | sp3d2-3 | $\frac{1}{\sqrt 6}\rm s-\frac{1}{\sqrt 2}\rm p\_y-\frac{1}{\sqrt 12}\rm d\_{z^2}-\frac{1}{2}\rm d\_{x^2-y^2}$ |
    |  | sp3d2-4 | $\frac{1}{\sqrt 6}\rm s+\frac{1}{\sqrt 2}\rm p\_y-\frac{1}{\sqrt 12}\rm d\_{z^2}-\frac{1}{2}\rm d\_{x^2-y^2}$ |
    |  | sp3d2-5 | $\frac{1}{\sqrt 6}\rm s-\frac{1}{\sqrt 2}\rm p\_z+\frac{1}{\sqrt 3}\rm d\_{z^2}$ |
    |  | sp3d2-6 | $\frac{1}{\sqrt 6}\rm s+\frac{1}{\sqrt 2}\rm p\_z+\frac{1}{\sqrt 3}\rm d\_{z^2}$ |
