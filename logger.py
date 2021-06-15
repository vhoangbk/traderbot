import logging

file_name_log = "log.txt"

def log(mesaage):
  logging.basicConfig(
    filename=file_name_log,
    filemode='a',
    format='%(asctime)s: %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
  )
  logging.info(mesaage)
