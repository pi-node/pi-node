// complianceMonitor.js
class ComplianceMonitor {
    constructor(threshold, penaltyFunction) {
        this.threshold = threshold; // Acceptable deviation from the stable value
        this.penaltyFunction = penaltyFunction; // Function to apply penalties
        this.currentValue = null;
    }

    updateValue(newValue) {
        this.currentValue = newValue;
        this.checkCompliance();
    }

    checkCompliance() {
        const targetValue = 314159.00; // Target stable value
        const deviation = Math.abs((this.currentValue - targetValue) / targetValue);

        if (deviation > this.threshold) {
            console.warn(`Non-compliance detected! Current value: ${this.currentValue}, Deviation: ${deviation}`);
            this.penaltyFunction();
        } else {
            console.log('Value is compliant with the stable value.');
        }
    }
}

module.exports = ComplianceMonitor;
