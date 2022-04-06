unameOut="$(uname -s)"
ROJO="\033[0;31m"
VERDE="\033[0;32m"
NO_OPTIMO="No existe solucion optima."

case "${unameOut}" in
    MINGW*)     
        PYTHON=python
        ;;
    *)
        PYTHON=python3
        ;;
esac

comprobar() {
    RES=$($PYTHON solucion.py $1 $2)
    SOL=$3

    if [ "$RES" = "$SOL" ]; then
        echo -e "${VERDE}Test ($1, $2, $3) Passed"
    else
        echo -e "${ROJO}Test ($1, $2, $3) failed"
        echo -e "Esperado: $SOL"
        echo -e "Recibido: $RES"
    fi
}

comprobar 200 "ejemplos/ej1.txt" "[5, 6]"
comprobar 500 "ejemplos/ej1.txt" "[5, 6, 2]"
comprobar 800 "ejemplos/ej1.txt" "$NO_OPTIMO"

comprobar 200 "ejemplos/ej2.txt" "[1, 7, 3]"
comprobar 450 "ejemplos/ej2.txt" "[1, 7, 3]"
comprobar 460 "ejemplos/ej2.txt" "[1, 7, 3, 2]"
comprobar 200 "ejemplos/ej3.txt" "[1, 2]"
comprobar 50 "ejemplos/ej4.txt" "[5]"
comprobar 100 "ejemplos/ej5.txt" "[4, 3]"
comprobar 50 "ejemplos/ej6.txt" "$NO_OPTIMO"
