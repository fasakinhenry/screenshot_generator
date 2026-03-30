# Constants
daily_extraction = 1200
selling_price = 20000
processing_cost_per_ton = 6000
fixed_cost = 10000000
royalty_rate = 0.05

# Efficiencies for 7 days
efficiencies = [0.75, 0.72, 0.78, 0.74, 0.76, 0.73, 0.77]

# Step 1: Calculate daily effective outputs
daily_outputs = []

for eff in efficiencies:
    output = daily_extraction * eff
    daily_outputs.append(output)

# Step 2: Total effective output
total_effective_output = sum(daily_outputs)

# Step 3: Total extracted (before efficiency loss)
total_extracted = daily_extraction * 7

# Step 4: Revenue
total_revenue = total_effective_output * selling_price

# Step 5: Processing cost
total_processing_cost = total_extracted * processing_cost_per_ton

# Step 6: Royalty
royalty = royalty_rate * total_revenue

# Step 7: Total cost
total_cost = total_processing_cost + fixed_cost + royalty

# Step 8: Net profit
net_profit = total_revenue - total_cost

# OUTPUTS
print("Daily Effective Outputs:")
for i, val in enumerate(daily_outputs, start=1):
    print(f"Day {i}: {val:.2f} tons")

print("\nTotal Effective Output:", total_effective_output)
print("Total Revenue: ₦", total_revenue)
print("Processing Cost: ₦", total_processing_cost)
print("Royalty: ₦", royalty)
print("Total Cost: ₦", total_cost)
print("Net Profit: ₦", net_profit)