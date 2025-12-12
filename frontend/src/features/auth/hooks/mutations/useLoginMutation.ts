import { useMutation } from '@tanstack/react-query';
import { authService } from '../../data/services/authService';
import { LoginInput } from '../../data/schemas/authSchemas';

export const useLoginMutation = () => {
    return useMutation({
        mutationFn: (data: LoginInput) => authService.login(data),
    });
};
