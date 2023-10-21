# my-pipeline
axs[0].errorbar(binmid, df_pip['T-value'], xerr = binstep, yerr = np.array(df_pip['T-errlo'], df_pip['T-errhi']),alpha = 0.6, label = 'yanling')
axs[1].errorbar(binmid, df_pip['Z-value'], xerr = binstep, yerr = np.array(df_pip['Z-errlo'], df_pip['Z-errhi']),alpha = 0.6)
axs[2].errorbar(binmid, df_pip['n-value'], xerr = binstep, yerr = np.array(df_pip['n-errlo'], df_pip['n-errhi']),alpha = 0.6)