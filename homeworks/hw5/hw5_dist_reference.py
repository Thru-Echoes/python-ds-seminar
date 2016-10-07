def dist(lat1, lon1, lat2, lon2):
    
    """
    This function calculates distance based on lat and lon
    """

    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    
    a = (np.sin(dlat/2))**2 + np.cos(lat1) * np.cos(lat2) * (np.sin(dlon/2))**2 
    c = 2 * np.arctan2( np.sqrt(a), np.sqrt(1-a) ) 
    d = 6373 * c # in km
    
    return d


def dist_list(attribute):
    
    """
    This functio returns distance lists for pair lists for both real distance and longitude distance
    """
    
    dist_list_r = []
    dist_list_l = []
    
    if attribute == 'Prep':
        pair_list = top10_corr_total_p.index.values
    elif attribute == 'MeanT':
        pair_list = top10_corr_total_mt.index.values
    
    for i in pair_list:

        real_dist = dist(float(top_modified[top_modified['ICAO'] == i[0]]['latitude_deg']),
                         float(top_modified[top_modified['ICAO'] == i[0]]['longitude_deg']), 
                         float(top_modified[top_modified['ICAO'] == i[1]]['latitude_deg']), 
                         float(top_modified[top_modified['ICAO'] == i[1]]['longitude_deg']))

        lon_dist = dist(0, float(top_modified[top_modified['ICAO'] == i[0]]['longitude_deg']),
                        0, float(top_modified[top_modified['ICAO'] == i[1]]['longitude_deg']))

        dist_list_r.append([i, real_dist])
        dist_list_l.append([i, lon_dist])
        
    dist_list_r = np.array(dist_list_r).transpose()
    dist_list_l = np.array(dist_list_l).transpose()
    
    return (dist_list_r, dist_list_l)