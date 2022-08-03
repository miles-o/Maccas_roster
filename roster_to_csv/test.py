shift_xpath = '/html/body/div[6]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/span[2]'           
shift_xpath = shift_xpath.split("/")
shift_xpath.insert(len(shift_xpath)-1, 'div[3]')
print(shift_xpath)
shift_xpath = '/'.join(shift_xpath)