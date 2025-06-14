#!/usr/bin/env node
/**
 * Benchmark script for sorting vs set creation performance comparison.
 * Updates benchmark_data.json with JavaScript results, preserving Python results.
 */

const fs = require('fs');
const path = require('path');

function genRandInts(n) {
    /**Generate n random integers.*/
    const arr = [];
    for (let i = 0; i < n; i++) {
        arr.push(Math.random());
    }
    return arr;
}

function sortArray(arr) {
    /**Sort array in-place.*/
    arr.sort((a, b) => a - b);
}

function makeSet(arr) {
    /**Create a Set from array.*/
    new Set(arr);
}

function bench(fn) {
    /**Benchmark a function and return execution time in milliseconds.*/
    const start = performance.now();
    fn();
    const end = performance.now();
    return end - start; // Already in milliseconds
}

function runBenchmarks() {
    /**Run benchmarks and return results.*/
    const benchmarkResults = [];
    const numRuns = 10;
    
    console.log("Running JavaScript benchmarks...");
    console.log(`Averaging over ${numRuns} runs per data point`);
    
    // warmup
    sortArray(genRandInts(100000));

    for (let pow = 1; pow < 24; pow++) {
        const n = 2 ** pow;
        console.log(`Testing n = ${n.toLocaleString()} (2^${pow})`);
        
        let totalSetTime = 0;
        let totalSortTime = 0;
        
        // Run multiple iterations and average
        for (let run = 0; run < numRuns; run++) {
            // Test Set creation
            const arr1 = genRandInts(n);
            const setTime = bench(() => makeSet(arr1));
            totalSetTime += setTime;
            
            // Test sorting  
            const arr2 = genRandInts(n);
            const sortTime = bench(() => sortArray(arr2));
            totalSortTime += sortTime;
        }
        
        // Calculate averages
        const avgSetTime = totalSetTime / numRuns;
        const avgSortTime = totalSortTime / numRuns;
        
        const result = {
            power: pow,
            n: n,
            setTime: avgSetTime,
            sortTime: avgSortTime,
            ratio: avgSetTime > 0 ? avgSortTime / avgSetTime : 0
        };
        
        benchmarkResults.push(result);
        console.log(`  Set: ${avgSetTime.toFixed(2)}ms, Sort: ${avgSortTime.toFixed(2)}ms, Ratio: ${result.ratio.toFixed(2)}`);
    }
    
    return benchmarkResults;
}

function main() {    
    // Run benchmarks
    const results = runBenchmarks();
    
    // Read existing data or create new structure
    const outputFile = path.join(__dirname, "benchmark_data.json");
    let data = {};
    
    try {
        if (fs.existsSync(outputFile)) {
            const existingData = fs.readFileSync(outputFile, 'utf8');
            data = JSON.parse(existingData);
        }
    } catch (error) {
        console.log("Creating new benchmark data file or reading existing one");
        data = {};
    }
    
    // Update only the JavaScript results
    data.javascript = results;
    
    // Save back to JSON file
    fs.writeFileSync(outputFile, JSON.stringify(data, null, 2));
    
    console.log(`\nBenchmark results saved to ${outputFile}`);
    console.log(`Generated ${results.length} data points for JavaScript`);
}

if (require.main === module) {
    main();
}
