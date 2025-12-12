import { useMutation } from '@tanstack/react-query';
import { authService } from '../../data/services/authService';
import { RegisterInput } from '../../data/schemas/authSchemas';

export const useRegisterMutation = () => {
    return useMutation({
        mutationFn: (data: RegisterInput) => authService.register(data),
    });
};
