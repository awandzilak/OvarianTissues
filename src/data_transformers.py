# data_transformers module
import pandas as pd

def to_ratios(df):
    """
    Calculates relevant ratios based on specific spectral bands and their sums (biomasses).
    
    Parameters:
    df (DataFrame): Input DataFrame containing spectral band and biomass data.
    
    Returns:
    DataFrame: DataFrame with calculated ratios.
    """
    df['Biomass I/Biomass II'] = df['Biomass_I']/df['Biomass_II']
    df['Amide III/Amide I'] = df['Band 1310']/df['Amide I']
    df['1080/1240'] = df['Band 1080']/df['Band 1240']
    df['1450/1390'] = df['Band 1450']/df['Band 1390']
    df['1080/Amide I'] = df['Band 1080']/df['Amide I']
    df['1240/Amide I'] = df['Band 1240']/df['Amide I']
    df['(1450+1390)/Lipids'] = (df['Band 1450']+df['Band 1390'])/df['Lipids']
    df['1450/Lipids'] = df['Band 1450']/df['Lipids']
    df['1390/Lipids'] = df['Band 1390']/df['Lipids']
    df['Amide B/Amide I'] = df['Band 3060']/df['Amide I']
    df['Amide III/Amide B'] = df['Band 1310']/df['Band 3060']
    df['CH3/1450'] = df['CH3 groups']/df['Band 1450']
    df['2850/1450'] = df['Band 2850']/df['Band 1450']
    
    # Drop unnecessary columns
    df.drop(['Lipids', 'Unsaturated lipids', 'CH3 groups', 'CH2 groups', 'Ester groups', 
             'Amide I','Alpha helix', 'Beta sheets', 'Beta turns',  
             'Band 1450', 'Band 1390', 'Band 1240', 'Band 1080', 'Band 1310', 
             'Band 2850', 'Band 3060', 'Biomass_I', 'Biomass_II', 'Biomass_Total'], 
            axis=1, inplace=True)
    
    return df
    
def outliers_lim_IQR(arr, n=1.5):
    """
    Finds limit values for outliers using the Interquartile Range (IQR) method.
    
    Parameters:
    arr (ndarray): Input array containing numerical data.
    n (float): Scaling factor to adjust the range of acceptable values (default is 1.5).

    Returns:
    tuple: Lower and upper limit values for outliers.
    """
    Q1 = np.percentile(arr, 25, axis=0)
    Q3 = np.percentile(arr, 75, axis=0)
    IQR = Q3 - Q1
    lower_lim = Q1 - n * IQR
    upper_lim = Q3 + n * IQR
    return lower_lim, upper_lim
    
def winsorize_outliers(arr, limits):
    """
    Winsorizes outliers in numeric columns of the given dataset.
    
    Parameters:
    arr (ndarray): Input array containing numerical data.
    limits (tuple): Tuple of lower and upper limit values for winsorization.

    Returns:
    ndarray: Array with outliers winsorized in the specified columns.
    """
    low, upp = limits
    for i in range(arr.shape[1]):
        col = arr[:, i]
        # Find the percentiles corresponding to the lower and upper limits obtained with IQR
        percentile_low = stats.percentileofscore(col, low[i]) / 100
        percentile_upp = 1 - stats.percentileofscore(col, upp[i]) / 100
        # Winsorize the data accordingly
        arr[:, i] = np.clip(col, np.percentile(col, percentile_low), np.percentile(col, percentile_upp))
    return arr
    

def outlim_to_tuple(df):
    """
    Convert DataFrame of outlier limits into a tuple of lower and upper bounds.
    """
    # Transpose the DataFrame to make rows become columns and vice versa
    df = df.T
    
    # Extract lower and upper bounds from transposed DataFrame
    lower = df[0]  # Lower bound values
    upper = df[1]  # Upper bound values
    
    # Return a tuple containing lower and upper bounds
    return tuple((lower, upper))
    