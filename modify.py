import netCDF4 as nc
import numpy as np

# Open the original NetCDF file
file_path = '2005-08-28_000000.nc'  # Replace with your file path
ds = nc.Dataset(file_path, 'r')

# Create a new NetCDF file for output
output_file = 'wrf_output_modified.nc'
ds_new = nc.Dataset(output_file, 'w', format='NETCDF4')

# Copy the global attributes from the original file
for attr_name in ds.ncattrs():
    ds_new.setncattr(attr_name, ds.getncattr(attr_name))

# Copy dimensions from the original file to the new file
for dim_name, dim in ds.dimensions.items():
    ds_new.createDimension(dim_name, len(dim) if not dim.isunlimited() else None)

# Function to check if a variable is empty and fill it with zeros if necessary
def get_or_fill_with_zeros(var, ref_shape):
    arr = ds.variables[var][:]
    if arr.size == 0:  # If the array is empty
        print(f"Variable '{var}' is empty, filling with zeros.")
        return np.zeros(ref_shape)
    return arr

# Copy and fill variables
for var_name, var in ds.variables.items():
    # Copy the variable's metadata (datatype, dimensions, etc.)
    out_var = ds_new.createVariable(var_name, var.datatype, var.dimensions)

    # If the variable is empty, fill it with zeros. Otherwise, copy the data.
    ref_shape = ds.variables['XLAT'].shape  # Use latitude's shape as a reference
    if var_name in ['T2', 'U10', 'V10']:  # Example variables to check
        data = get_or_fill_with_zeros(var_name, ref_shape)
    else:
        data = ds.variables[var_name][:]  # Copy original data if not empty

    # Write the data to the new NetCDF file
    out_var[:] = data

    # Copy variable attributes
    for attr_name in var.ncattrs():
        out_var.setncattr(attr_name, var.getncattr(attr_name))

# Close the datasets
ds.close()
ds_new.close()

print(f"Modified NetCDF file saved as {output_file}")