# Distance lists for precipitation and temperature
dist_p = dist_list('Prep')
dist_t = dist_list('MeanT')

Prep_df = pd.DataFrame([dist_p[0][0], dist_p[0][1], dist_p[1][1],
                        prep_corr_1[1] ,prep_corr_3[1], prep_corr_7[1]]).transpose()

Prep_df.columns = ['icao', 'real_dist', 'lon_dist', 'prep_1', 'prep_3', 'prep_7']

T_df = pd.DataFrame([dist_p[0][0], dist_p[0][1], dist_p[1][1],
                     t_corr_1[1], t_corr_3[1], t_corr_7[1]]).transpose()

T_df.columns = ['icao', 'real_dist', 'lon_dist', 't_1', 't_3', 't_7']

temp = Prep_df.sort('real_dist')
f, ax = plt.subplots()
ax.plot(temp['real_dist'], temp['prep_1'], label='Real dist 1 day') 
ax.legend()
ax.plot(temp['real_dist'], temp['prep_3'], label='Real dist 3 day')
ax.legend()
ax.plot(temp['real_dist'], temp['prep_7'], label='Real dist 7 day')
ax.legend()
ax.set_title('Precipitation correlation (Real distance)')
ax.set_xlabel('Distance')
ax.set_ylabel('Correlation strength')