# Remove if it exists
if [ -f lab-password.zip ]; then
  rm lab-password.zip
fi

# And recreate
zip -j lab-password.zip ./public/task.pdf ./public/scripts/server.py