#!/usr/bin/env python3

import gevent
import os
import sys
import pandas as pd


class Monitor:
    def __init__(self, columns, save_dir, name, do_monitor):
        self.do_monitor = do_monitor
        if save_dir is None:
            self.do_monitor = False
        if self.do_monitor:
            self.df = pd.DataFrame(columns=columns)
            self.save_path = save_dir + name + ".csv"
            self.lock = gevent.lock.Semaphore()
            # Better try saving now
            self.save()

    def save(self):
        if self.do_monitor:
            dir_path = os.path.dirname(self.save_path)
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path)

            try:
                self.lock.acquire()
                self.df.to_csv(self.save_path, index=False)
                self.lock.release()
            except:
                e = sys.exc_info()[0]
                raise OSError("Could not save to {}: {}".format(
                    self.save_path, str(e)))
            # else:
            #     print("Successfully saved {}. {} lines.".format(
            #         self.save_path, self.df.shape[0]))

    def put(self, line):
        if self.do_monitor:
            if len(line) != len(self.df.columns):
                print("Columns:", self.df.columns)
                print("Line:", line)
                raise ValueError(
                    "Come back when you learnt to count:"
                    " invalid columns number")

            new_row = dict(zip(self.df.columns, line))
            self.lock.acquire()
            self.df = self.df.append(new_row, ignore_index=True)
            self.lock.release()
