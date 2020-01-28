
let generate_initial = (chance) => {

    let gain = 2 - (chance / 100).toFixed(2);
    let lose = 1 * (chance / 100).toFixed(2);
    lose = (lose < 0.5) ? 0.5 : lose;
    return {
        "gain": gain, "lose": lose
    }
}
let input = [
    {
        "option" : "A",
        "chance" : 75,
        "probs" : generate_initial(75)
    },
    {
        "option": "B",
        "chance": 25,
        "probs": generate_initial(25)
    }
];

let values = [5,10,20,30,40,50,100,150,200,250,300,350,400,450,500,600,700,800,900,1000]; 

let predictions = [];

let input_size = 10;

for (i = 0; i < input_size; i++){

    let value_index = Math.floor(Math.random() * values.length);
    let option_index = Math.floor(Math.random() * input.length);
    predictions.push(
        {
            'value' : values[value_index],
            'option': input[option_index]["option"],
            'probs' : input[option_index]["probs"]
        }
    )
}

let generate_result = (predictions,winner)=>{

    let result = {
        "options": {}, "in": 0, "out": 0
    }
    predictions.map((v) => {
        result.in  = (v.option != winner) ? result.in + (v.probs["lose"] * v.value) : result.in;
        result.out = (v.option == winner) ? result.out + (v.probs["gain"] * v.value) : result.out;
        result.options[v.option] = (result.options[v.option] + 1) || 1;
    })
    return result;
}

input.map( (i) => {
    let result = generate_result(predictions,i.option);
    console.log(`If ${i.option} be the option result :`)
    console.log(" *********")
    console.log(` Total choices : ${result.options[i.option]}`)
    console.log(` Inside  : ${result.in}`);
    console.log(` Outside : ${result.out}`);
    let diff = result.in - result.out;
    console.log(`The difference is : ${diff}`);
    console.log(" *********");
});

