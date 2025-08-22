
function rollDie(sides=6) {
    return Math.floor(Math.random() * sides) + 1;
}
function roll2d6() {
    return rollDie(6) + rollDie(6);
}
