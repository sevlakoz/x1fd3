import os
from dataclasses import dataclass
from configparser import ConfigParser
from typing import Dict, Any, List, Tuple
import numpy as np
import numpy.typing as npt
from scipy.optimize import least_squares  # type: ignore
from scipy.interpolate import splrep, splev  # type: ignore
from scipy.linalg import eigh_tridiagonal  # type: ignore

# =======================================================================
# =======================================================================


@dataclass
class Level:
    energy: float
    rot_const: float
    r_grid: npt.NDArray[np.float_]
    wavef_grid: npt.NDArray[np.float_]


# =======================================================================
# =======================================================================


def print_input_file(fname: str) -> None:

    if os.path.isfile(fname):
        print(f"\n=== Input file: {fname} ===\n")
        with open(fname) as inp:
            for line in inp:
                print(line, end="")
        print(f"\n=== End of input file: {fname} ===\n")
    else:
        exit(f"ERROR: No such file: {fname}")


# =======================================================================


def print_pecs(
    rp: npt.NDArray[np.float_],
    up: npt.NDArray[np.float_],
    params: Dict[str, Any],
) -> None:

    hdr = f'U({params["ptype"]}),cm-1'
    print(f'{"R,A":>10}{"U(p-w),cm-1":>20}{hdr:>20}{"delta,cm-1":>20}')
    # loop over r
    for r, u in zip(rp, up):
        if params["ptype"] == "EMO":
            ua = emo(
                r,
                params["de"],
                params["re"],
                params["rref"],
                params["q"],
                params["beta"],
            )
        print(f"{r:10.5f}{u:20.5f}{ua:20.5f}{u - ua:20.5f}")


# =======================================================================


def print_params(params: Dict[str, Any]) -> None:

    print(f"[{params['ptype']}]")
    print(f"de    {params['de']}")
    print(f"re    {params['re']}")
    print(f"rref  {params['rref']}")
    print(f"q     {params['q']}")

    print("beta  ", end="")
    for b in params["beta"]:
        print(f"{b}\n      ", end="")
    print()


# =======================================================================


def print_levels(levels: Dict[int, Dict[int, Level]]) -> None:

    print("\n=== Energy levels ===")
    for j in levels.keys():
        print(f'\nJ = {j}\n{"v":>3}{"E,cm-1":>15}{"Bv,cm-1":>15}')
        for v, lev in levels[j].items():
            print(f"{v:3d}{lev.energy:15.5f}{lev.rot_const:15.8f}")


# =======================================================================


def print_matrix_elements(
    params: Dict[str, Any],
    levels: Dict[int, Dict[int, Level]],
    matrix_elements: Dict[int, Dict[int, Level]],
) -> None:

    print("\n=== Transition energies & Intergals <f(v',J')|d|f(v'',J'')>,D ===\n")
    print(f"v'' = {params['v1']}")
    print(f"v'  = {params['v2']}\n")

    for j2 in range(params["jmax"] + 1):
        print(f"J' = {j2}")
        print(f"""{"J''":>4}{"E',cm-1":>15}{"E'',cm-1":>15}{"<f'|d|f''>,D":>15}""")
        for j1 in range(params["jmax"] + 1):
            e2 = levels[j2][params["v2"]].energy
            e1 = levels[j1][params["v1"]].energy
            print(f"{j1:4d}{e2:15.5f}{e1:15.5f}{matrix_elements[j2][j1]:15.5e}")
        print()


# =======================================================================


def print_levels_n_expdata(
    params: Dict[str, Any],
    levels: Dict[int, Dict[int, Level]],
    expdata: Dict[int, Dict[int, float]],
) -> None:

    print(f'\n{"J":>4}{"v":>4}{"Eexp,cm-1":>15}{"Ecalc,cm-1":>15}{"delta,cm-1":>15}')
    for j in expdata.keys():
        if j > params["jmax"]:
            continue
        for v in expdata[j].keys():
            ee = expdata[j][v]
            ec = levels[j][v].energy
            print(f"{j:4d}{v:4d}{ee:15.5f}{ec:15.5f}{ee - ec:15.5f}")
    print()


# =======================================================================
# =======================================================================


def read_pw_curve(
    fname: str,
) -> Tuple[npt.NDArray[np.float_], npt.NDArray[np.float_]]:

    r = []
    c = []

    # read pec
    with open(fname) as inp:
        for line in inp:
            if line.lstrip() == "" or line.lstrip()[0] == "#":
                continue
            line = line.split()  # type: ignore
            r.append(float(line[0]))
            c.append(float(line[1]))

    # check
    if len(r) == 0:
        exit(f"No PEC point found in {fname}")

    r = np.array(r)  # type: ignore
    c = np.array(c)  # type: ignore

    return r, c  # type: ignore


# =======================================================================


def read_pec_params(fname: str) -> Dict[str, Any]:

    input_parser = ConfigParser(delimiters=(" ", "\t"))
    input_parser.read(fname)

    params = {}

    if len(input_parser.sections()) > 1:
        exit(f'ERROR: Two or more analytic functions given in "{fname}"')

    ptype = input_parser.sections()[0]

    if not ptype in ["EMO"]:
        exit(f'ERROR:  Uknown potential type "{ptype}"')

    for keyword, value in input_parser[ptype].items():
        if keyword in ("q"):
            params[keyword] = int(value)
        elif keyword in ("re", "de", "rref"):
            params[keyword] = float(value)  # type: ignore
        elif keyword in ("beta"):
            params[keyword] = np.array(list(map(float, value.split())))  # type: ignore

    params_check = {"EMO": set(["re", "de", "rref", "q", "beta"])}

    if set(params.keys()) != params_check[ptype]:
        exit(
            f"ERROR:  for {ptype} the following parameters must be given: {params_check[ptype]}"
        )

    params["ptype"] = ptype  # type: ignore

    return params


# =======================================================================


def read_vr_calc_params(fname: str, rtype: str) -> Dict[str, Any]:

    if not rtype in ["ENERGY", "SPECTRUM", "FIT"]:
        exit(f'ERROR:  Uknown run type "{rtype}"')

    # read calc params
    input_parser = ConfigParser(delimiters=(" ", "\t"))
    input_parser.read(fname)

    params = {}

    if len(input_parser.sections()) > 1:
        exit(f'ERROR: Two or more sets of parameters given in "{fname}"')

    if input_parser.sections()[0] != rtype:
        exit(f'ERROR: run type in "{fname}" is not consistent with the actual run type')

    for keyword, value in input_parser[rtype].items():
        if keyword in ("jmax", "v1", "v2"):
            params[keyword] = int(value)
        elif keyword in ("mass1", "mass2", "rmin", "rmax"):
            params[keyword] = float(value)  # type: ignore

    params_check = {
        "ENERGY": set(["mass1", "mass2", "rmin", "rmax", "jmax"]),
        "SPECTRUM": set(["mass1", "mass2", "rmin", "rmax", "jmax", "v1", "v2"]),
        "FIT": set(["mass1", "mass2", "rmin", "rmax"]),
    }

    if set(params.keys()) != params_check[rtype]:
        exit(
            f"ERROR:  for {rtype} the only following parameters must be given: {params_check[rtype]}"
        )

    params["rtype"] = rtype  # type: ignore

    return params


# =======================================================================


def emo(
    r: float, de: float, re: float, rref: float, q: int, beta: List[float]
) -> List[float]:

    # EMO calc
    y = (r ** q - rref ** q) / (r ** q + rref ** q)

    beta_pol = beta[0]
    for n in range(1, len(beta)):
        beta_pol += beta[n] * y ** n

    return de * (1 - np.exp(-beta_pol * (r - re))) ** 2  # type: ignore


# =======================================================================


def res_pec(
    guess: List[float],
    rp: npt.NDArray[np.float_],
    up: npt.NDArray[np.float_],
    params: Dict[str, Any],
) -> List[float]:

    # fitted params
    de = guess[0]
    re = guess[1]
    beta = guess[2:]

    # residual calc
    res = []

    for r, u in zip(rp, up):
        if params["ptype"] == "EMO":
            ua = emo(r, de, re, params["rref"], params["q"], beta)
        e = max(u / 100.0, 100.0)
        res.append((ua - u) / e)

    return res


# =======================================================================


def pec_fit(
    rp: npt.NDArray[np.float_],
    up: npt.NDArray[np.float_],
    params: Dict[str, Any],
) -> Tuple[Dict[str, Any], str, bool]:

    # fitted params
    guess = [params["de"], params["re"]]
    guess.extend(params["beta"])
    add_args = (rp, up, params)

    # scipy least squares
    res_1 = least_squares(res_pec, guess, args=add_args)

    # out
    tmp = {} | params
    tmp["de"] = res_1.x[0]
    tmp["re"] = res_1.x[1]
    tmp["beta"] = np.array(list(res_1.x[2:]))

    return tmp, res_1.message, res_1.success


# =======================================================================


def vr_solver(
    ptype: str,
    params: Dict[str, Any],
    rp: npt.NDArray[np.float_] = np.zeros(1, dtype=float),
    up: npt.NDArray[np.float_] = np.zeros(1, dtype=float),
) -> Dict[int, Dict[int, Level]]:

    # physical constants
    au_to_Da = 5.48579909065e-4
    au_to_cm = 219474.63067
    a0_to_A = 0.529177210903

    # grid point number
    ngrid = 50000

    # reduced mass
    mu = params["mass1"] * params["mass2"] / (params["mass1"] + params["mass2"])

    # h^2 / (2*mu) [cm-1 * A^2]
    scale = au_to_Da * au_to_cm * a0_to_A ** 2 / (2 * mu)

    # grid
    step = (params["rmax"] - params["rmin"]) / (ngrid - 1)
    r_grid = np.linspace(params["rmin"], params["rmax"], ngrid)

    if ptype == "pw":
        # cubic spline for pec
        spl_pec = splrep(rp, up)
        u_grid = splev(r_grid, spl_pec)
        emax = u_grid[-1]
    elif ptype == "an":
        # EMO
        if params["ptype"] == "EMO":
            u_grid = np.array(
                list(
                    map(
                        lambda x: emo(
                            x,
                            params["de"],
                            params["re"],
                            params["rref"],
                            params["q"],
                            params["beta"],
                        ),
                        r_grid,
                    )
                )
            )
            emax = params["de"]
    else:
        exit(f'ERROR:  Uknown pec type "{ptype}"')

    # loop over J to calculate level energies
    levels: Dict[int, Dict[int, Level]] = {}

    for j in range(params["jmax"] + 1):

        # diagonal elements (ngrid)
        diagonal = u_grid / scale + j * (j + 1) / r_grid ** 2 + 2 * step ** -2

        # off-diagonal elements (ngrid-1)
        off_diag = np.full(ngrid - 1, -(step ** -2))

        # SciPy routine to calculate eigenvalues and eigenvectors
        results = eigh_tridiagonal(
            diagonal, off_diag, select="v", select_range=(0.0, emax / scale)
        )

        # out
        levels[j] = {}
        for v, en in enumerate(results[0]):
            wf = results[1][:, v]

            # correction for fd3 scheme
            fd_cor = step ** 2 / scale / 12 * np.sum((wf * (u_grid - en * scale)) ** 2)

            # vr level
            lev = Level(
                en * scale + fd_cor, scale * np.sum(wf ** 2 / r_grid ** 2), r_grid, wf
            )
            levels[j][v] = lev

    return levels


# =======================================================================


def me_calc(
    params: Dict[str, Any],
    levels: Dict[int, Dict[int, Level]],
    rd: npt.NDArray[np.float_],
    fd: npt.NDArray[np.float_],
) -> Dict[int, Dict[int, Level]]:

    # cubic spline to find DM values
    r_grid = levels[0][0].r_grid
    spl_dip = splrep(rd, fd)
    d_grid = splev(r_grid, spl_dip)

    # matrix elements calc
    matrix_elements: Dict[int, Dict[int, Level]] = {}

    for j2 in range(params["jmax"] + 1):
        matrix_elements[j2] = {}
        for j1 in range(params["jmax"] + 1):
            matrix_elements[j2][j1] = np.sum(
                levels[j1][params["v1"]].wavef_grid
                * levels[j2][params["v2"]].wavef_grid
                * d_grid
            )

    return matrix_elements


# =======================================================================


def read_expdata(fname: str) -> Dict[int, Dict[int, float]]:

    input_parser = ConfigParser(delimiters=(" ", "\t"))
    input_parser.read(fname)

    # read levels
    expdata = {}
    n_levels = 0

    for j in input_parser.sections():
        tmp = {}
        for v, e in input_parser[j].items():
            tmp[int(v)] = float(e)
            n_levels += 1
        expdata[int(j)] = tmp

    # check
    if n_levels == 0:
        exit(f"No energy levels found in {fname}")

    return expdata


# =======================================================================


def res_exp(
    guess: List[float],
    params: Dict[str, Any],
    rp: npt.NDArray[np.float_],
    up: npt.NDArray[np.float_],
    expdata: Dict[int, Dict[int, float]],
) -> List[float]:

    # fitted params
    tmp = {} | params

    tmp["de"] = guess[0]
    tmp["re"] = guess[1]
    tmp["beta"] = guess[2:]

    levels = vr_solver("an", tmp)

    # residual calc
    res = []

    # exp levels
    for j in expdata.keys():
        for v in expdata[j].keys():
            res.append((levels[j][v].energy - expdata[j][v]) / 0.1)

    # pec
    for r, u in zip(rp, up):
        ua = emo(r, tmp["de"], tmp["re"], tmp["rref"], tmp["q"], tmp["beta"])
        e = max(u / 100.0, 100.0)
        res.append((ua - u) / e)

    return res


# =======================================================================


def exp_fit(
    params: Dict[str, Any],
    rp: npt.NDArray[np.float_],
    up: npt.NDArray[np.float_],
    expdata: Dict[int, Dict[int, float]],
) -> Tuple[Dict[str, Any], str, bool]:

    # fitted params
    guess = [params["de"], params["re"]]
    guess.extend(params["beta"])
    add_args = (params, rp, up, expdata)

    # scipy least squares
    res_1 = least_squares(res_exp, guess, args=add_args)

    # out
    tmp = {} | params
    tmp["de"] = res_1.x[0]
    tmp["re"] = res_1.x[1]
    tmp["beta"] = np.array(list(res_1.x[2:]))

    return tmp, res_1.message, res_1.success


# =======================================================================
