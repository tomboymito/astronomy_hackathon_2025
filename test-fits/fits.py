from astropy.io import fits

# Создаем PrimaryHDU с пустыми данными
hdu = fits.PrimaryHDU()

# Добавляем необходимые заголовки
hdu.header['SIMPLE'] = True
hdu.header['BITPIX'] = 8
hdu.header['NAXIS'] = 0
hdu.header['H_MAG'] = 15.0    # Абсолютная звёздная величина
hdu.header['ALBEDO'] = 0.04  # Альбедо

# Сохраняем в файл
hdu.writeto('test-fits/example.fits', overwrite=True)