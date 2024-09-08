import netCDF4 as nc

# Open the NetCDF file
file_path = '2005-08-28_000000.nc'  # Replace with the actual file path
ds = nc.Dataset(file_path)

# Print general information about the NetCDF file
print(ds)

# List all available variables
print("\nVariables available in the file:\n")
for var in ds.variables:
    print(var)

# Optionally, you can print details of specific variables
# For example, printing detailed info of 'T2' variable (2m temperature)
variable_name = 'T2'  # Replace with your chosen variable name
if variable_name in ds.variables:
    print(f"\nDetails of variable '{variable_name}':\n")
    print(ds.variables[variable_name])

# Close the NetCDF file
ds.close()
