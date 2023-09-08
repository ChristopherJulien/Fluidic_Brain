    def get_continuous_pressure(self, duration_s, interval_s):
        assert duration_s > 0
        assert interval_s > 0.001
        pressure_list = []
        time_list = []
        fgt_init()
        t_start = time.time()
        t_end = time.time() + duration_s
        while time.time() < t_end:
            measurement = fgt_get_pressure(0)
            pressure_list.append(measurement)
            print('Current pressure {:0.2f} mbar  Time:{:0.2f}'.format(
                measurement, time.time()-t_start))
            time_list.append(time.time()-t_start)
            time.sleep(interval_s)
        fgt_close()
        return pressure_list, time_list