dog = {
    breed : 'Bulldog',
    dates : [1, 2, 3, 4, 5],
    goals : [0, 0, 4, 5, 6]
}

bread = {
    dates : [1, 2, 3, 4, 5],
    goals : [0, 3, 4, 5, 6]
}

labels = [0, 1, 3, 4, 5]


function removeEmpty(array) {
    return array.reduce( (a, v) => a + v)

} 


for (let date of labels) {
    removeEmpty(dog.goals)
    removeEmpty(bread.goals)
}

console.log(dog.goals)
console.log(bread.goals);
